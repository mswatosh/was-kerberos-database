# was-kerberos-database

## This is an experimentation environment for Database access on WebSphere with Kerberos. Practices demonstrated here are not necessarily recommended or secure. Use at your own risk.

### Overview

The docker compose environment sets up a KDC , Database (DB2), and an application server (WebSphere traditional or Liberty) with kerberos configured in each image. 

May require OpenJ9 Java 8. Tested with OpenJ9/OpenJDK 1.8.0_232

Bring up the WebSphere traditional environment with:
```
./gradlew libertyPackage
docker-compose build
docker-compose up
```
### WebSphere traditional 
Also needs `./gradlew libertyPackage` run to copy the db2 driver and app to the correct directory.

`keberos.py` is the admin script for configuring kerberos and datasources  
`installApps.py` is the admin script for installing the application



The application can be accessed at the endpoint:  
http://localhost:9080/was-kerberos-database/example  
username: dbuser
password: password

Admin Console: https://localhost:9043/ibm/console/  
User: wsadmin  
Password: password

WSAdmin testing:  
`/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -conntype NONE -lang jython`

### Liberty
**Liberty doesn't support accessing databases using kerberos**

The Liberty environment is in liberty.yml
```
./gradlew libertyPackage
docker-compose -f liberty.yml build
docker-compose -f liberty.yml up
```

Once the environment is up (db2 usually takes the longest to start) this endpoint can be used to access the database:  
http://localhost:9080/was-kerberos-database/example
Which will respond with:  `java.sql.SQLInvalidAuthorizationSpecException: [jcc][t4][201][11237][4.25.13] Connection authorization failure occurred. Reason: Security mechanism not supported. `  
This shows that DB2 won't accept user/password, because it is expecting kerberos authentication.

### Liberty with SQLServer
**Liberty doesn't support accessing databases using kerberos**

The compose environment for Liberty with SQL Server is liberty-mssql.yml  
Currently there is no kerberos configured for SQLServer

SQLServer cmd line  
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P P@ssw0rd

```
SELECT auth_scheme FROM sys.dm_exec_connections  
GO
```

Currently getting the following when trying to login locally without user/pass:
```
2020-03-03 21:32:10.75 Logon       Error: 18452, Severity: 14, State: 1.
2020-03-03 21:32:10.75 Logon       Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication. [CLIENT: 10.5.0.5]
```
`Error: 18452, Severity: 14, State: 1 - The login may use Windows Authentication but the login is an unrecognized Windows principal. An unrecognized Windows principal means that Windows can't verify the login. This might be because the Windows login is from an untrusted domain.`

My guess is this is due to the lack of Active Directory server, and that this will not be possible without one.

https://github.com/microsoft/mssql-docker/issues/165

### Kerberos
Realm: EXAMPLE.COM  
User: dbuser@EXAMPLE.COM  
User: wsadmin@EXAMPLE.COM  
WAS Service: wassrvc/websphere@EXAMPLE.COM  
DB2 Service: db2srvc@EXAMPLE.COM  
DB2 User: db2inst1@EXAMPLE.COM  


### DB2
The Dockerfile installs kerberos libs, and copies `docker-entrypoint.sh` and `createschema.sh` into the image.  
`docker-entrypoint.sh` creates the krb5.conf and starts the database.  
`createschema.sh` updates the database configuration for kerberos, runs kinit with the user, and starts db2 admin.

The db2 user account is db2inst1@EXAMPLE.COM 
The db2 kerberos service is db2srvc@EXAMPLE.COM

We call kinit before db2start because db2 looks for credentials in the ccache.

DB2 Logs: /database/config/db2user/sqllib/db2dump/DIAG0000/

### Links
[Configure Kerberos in WAS](https://www.ibm.com/support/knowledgecenter/en/SSEQTP_9.0.5/com.ibm.websphere.base.doc/ae/tsec_kerb_setup.html)  
[Configure Kerberos in DB2](https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.db2.luw.admin.sec.doc/doc/c0058525.html)