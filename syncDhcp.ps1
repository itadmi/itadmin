param(
[string]$DBServer=$(throw "please input dbserver ip"),
[string]$Database=$(throw "please input db"),
[string]$user=$(throw "please input db user"),
[string]$password= $(throw "please input db passwd"),
[string]$dhcpid= $(throw "please input dhcp computerName")
)




$dhcpLease = Get-DhcpServerv4Scope | Get-DhcpServerv4Lease
$leaseDict = @{}
foreach ( $l in $dhcpLease )
{
    $dict = @{}
    $dict.ipaddress = $l.ipaddress.ipaddresstostring
    $dict.clientid = $l.ClientId.replace('-','')
    $dict.hostname = $l.HostName
    $dict.scopeid = $l.scopeid
    $leaseDict[$dict.clientid] = $dict
}




try {
    $connectionString = "Data Source=$DBServer;Initial Catalog=$Database;user id=$user;pwd=$password"
    write-host $connectionString
    $Connection = New-Object System.Data.SQLClient.SQLConnection
    $Connection.ConnectionString = $connectionString

    $Command = New-Object System.Data.SQLClient.SQLCommand
    $Command.Connection = $Connection
    $Connection.Open()
}
catch [exception] {
    Write-Warning ('Connect to database failed with error message:{0}' -f ,$_)
    $SqlConnection.Dispose()
    return $null
}
try {
    $CommandText = "Select clientid,scopeid,hostname,dhcpid from [switch_dhcplease]"
    $command = $connection.CreateCommand()
    $command.CommandText = $CommandText
    $result = $command.ExecuteReader()
    $table = new-object “System.Data.DataTable”
    $table.Load($result)
}
catch [exception] {
    Write-Warning ('Connect to database failed with error message:{0}' -f ,$_)
    $SqlConnection.Dispose()
    return $null
}

$results = @{}
foreach ( $row in $table )
{
     $results[$row.clientid] =  $row       
}

foreach ( $dict in $leaseDict.Values)
{
   
    $clientid  = $dict.clientid
    $scopeid   = $dict.scopeid
    $hostname  = $dict.hostname
    if ( $hostname.Length -gt 50 ) { $hostname = $hostname.Substring(0,49) }
    try
    {
        $result = $results[$clientid]

        if (($dhcpid -ne $result['dhcpid']) -or ($hostname -ne $result['hostname']))
        {

            try
            {
                $CommandText =  "Update [switch_dhcplease] set scopeid='" + $scopeid + "', hostname='" + $hostname + "',dhcpid='" + $dhcpid + "' where clientid = '" + $clientid + "'"
                $Command.CommandText = $CommandText
	            $Command.ExecuteNonQuery()

            }
            catch [exception] {
                write-host 'adadfadsfasdfasdf'
            }
        }
    }
    catch [exception] {
        $CommandText = "insert into [switch_dhcplease] ( [clientid], [scopeid], [hostname], [dhcpid]) values ('" +  $clientid + "', '" + $scopeid + "','" + $hostname + "','" + $dhcpid + "')"
        try {
            $Command.CommandText = $CommandText
	        $Command.ExecuteNonQuery()
   
        }
        catch {
            write-host $CommandText ,'insert into fault!!!'
        }
    }   
   
}

$Connection.Close()