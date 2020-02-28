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
username: db2user/websphere  
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


### Kerberos
Realm: EXAMPLE.COM  
User: db2user/db2@EXAMPLE.COM  
User: db2user/websphere@EXAMPLE.COM  
User: wsadmin@EXAMPLE.COM


### DB2
The Dockerfile installs kerberos libs, and copies `docker-entrypoint.sh` and `createschema.sh` into the image.  
`docker-entrypoint.sh` creates the krb5.conf and starts the database.  
`createschema.sh` updates the database configuration for kerberos, runs kinit with the user, and starts db2 admin.

DB2 Logs: /database/config/db2user/sqllib/db2dump/DIAG0000/

### Links
[Configure Kerberos in WAS](https://www.ibm.com/support/knowledgecenter/en/SSEQTP_9.0.5/com.ibm.websphere.base.doc/ae/tsec_kerb_setup.html)  
[Configure Kerberos in DB2](https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.db2.luw.admin.sec.doc/doc/c0058525.html)