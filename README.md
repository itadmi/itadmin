ubuntu 18 + django +python3.6+mssql

Pyodbc driver ：
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15



curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
apt-get install msodbcsql17
apt-get install mssql-tools
apt-get install unixodbc-dev
cat /etc/odbc.ini 
cat /etc/odbcinst.ini 


apt install python3-pip
pip3 install django
pip3 install pysnmp pyasn1
pip3 install django-pyodbc-azure pyodbc



1:uploadFile：
  mkdir /itadmin

2:update itadmin/setting.py
  ALLOW-HOST
  DATABASES

3:
  Python3 /itadmin/manager.py makemigrations
  Python3 /itadmin/manager.py migrate

4:set table switch_uselogin field logintime 
  switch_userlogin logintime default Value or Binding  (getdate())

5:create user
  Python3 /itadmin/manager.py createsuperuser

6:crontab –e
  */10 * * * * /usr/bin/python3 /itadmin/manage.py getData
  * */12 * * * /usr/bin/python3 /itadmin/manage.py clearData

