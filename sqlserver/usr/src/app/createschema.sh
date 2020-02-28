#wait for the SQL Server to come up
sleep 45s

hostname sqlserver

#run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P P@ssw0rd -d master -i /usr/src/app/setup.sql