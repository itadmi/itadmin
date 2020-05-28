Dim con
Set objSysInfo = CreateObject("ADSystemInfo")
strUser = objSysInfo.UserName
Set objUser = GetObject("LDAP://" & strUser)

UserName = objUser.sAMAccountName
displayName = objUser.displayName
telephone = objUser.telephoneNumber

Set WshNetwork = WScript.CreateObject("WScript.Network")
ComputerID = WshNetwork.ComputerName


Set objArgs = WScript. Arguments
connStr = "driver={sql server};Server=" + objArgs(0) +";Database="+objArgs(1)+";uid="+objArgs(2)+"pwd="+objArgs(3)+";"

set con = wscript.CreateObject("ADODB.Connection")

con.Open connStr
command = "delete from switch_UserLogin where ComputerID = '"  + ComputerID +  "' and UserName = '" + UserName + "'"
con.Execute(command)

command = "insert into switch_UserLogin (UserName,displayName,Telephone,ComputerID) values ('"
command = command + UserName + "','" + displayName  + "','"  + telephone + "','" + ComputerID +"')"

con.Execute(command)

con.Close()

