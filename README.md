# was-kerberos-database

## This is an experimentation environment for Database access on WebSphere with Kerberos. Practices demonstrated here are not necessarily recommended or secure. Use at your own risk.

### Overview

The docker compose environment sets up a KDC , Database (DB2), and an application server (WebSphere traditional or Liberty) with kerberos configured in each image. 

May require OpenJ9 Java 8. Tested with OpenJ9/OpenJDK 1.8.0_232

### WebSphere traditional 

Bring up the WebSphere traditional environment with:

``` sh
./gradlew libertyPackage #create app and copy database drivers
docker-compose build
docker-compose up
```

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

WebSphere traditional trace is available at:
`/trace/twas`

### Liberty

**Liberty doesn't support accessing databases using kerberos**

The Liberty environment is in `liberty.yml`

#### DB2

The compose environment for Liberty with DB2 is `liberty-db2.yml`

```sh
./gradlew libertyPackage
docker-compose -f liberty.yml build
docker-compose -f liberty.yml up
```

Once the environment is up (db2 usually takes the longest to start) this endpoint can be used to access the database:  
http://localhost:9080/was-kerberos-database/example

#### SQLServer

The compose environment for Liberty with SQLServer is `liberty-mssql.yml` 
Currently there is no kerberos configured for SQLServer

```sh
./gradlew libertyPackage
docker-compose -f liberty-mssql.yml build
docker-compose -f liberty-mssql.yml up
```

SQLServer cmd line  
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P P@ssw0rd

```sql
SELECT auth_scheme FROM sys.dm_exec_connections  
GO
```

Currently getting the following when trying to login locally without user/pass:
```txt
2020-03-03 21:32:10.75 Logon       Error: 18452, Severity: 14, State: 1.
2020-03-03 21:32:10.75 Logon       Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication. [CLIENT: 10.5.0.5]
```

```txt
Error: 18452, Severity: 14, State: 1 - The login may use Windows Authentication but the login is an unrecognized Windows principal. An unrecognized Windows principal means that Windows can't verify the login. This might be because the Windows login is from an untrusted domain.
```

My guess is this is due to the lack of Active Directory server, and that this will not be possible without one.

https://github.com/microsoft/mssql-docker/issues/165

#### Oracle

The compose environment for Liberty with Oracle is `liberty-oracle.yml`
Currently there is no kerberos configured for Oracle

```sh
./gradlew buildOracleBase
./gradlew libertyPackage
docker-compose -f liberty-oracle.yml build
docker-compose -f liberty-oracle.yml up
docker-compose -f liberty-oracle.yml down -v #Bring down and remove volume (so oracle data is not persisted)
```


Note: If you see the following error when running `./gradlew buildOracleBase` you may need to increase your Disk image size under Docker Settings -> Resources.
```txt
checkSpace.sh: ERROR - There is not enough space available in the docker container.
```

Access oracle using sqlplus:
```sh
# Access oracle using default (BEQ) authentication
docker exec -it --user oracle was-kerberos-database_oracle_1 /bin/sh -c 'sqlplus / as sysdba'

# Access oracle using Kerberos Authentication
docker exec -it --user oracle was-kerberos-database_oracle_1 /bin/sh -c 'sqlplus /@XE'

# Interactive access to oracle using Kerberos Authentciation 
$ docker exec -it oracle was-kerberos-database_oracle_1
sh-4.2$ su oracle
[oracle@oracle /]$ sqlplus /@XE
```

Access oracle container:
`docker exec -it was-kerberos-database_oracle_1 /bin/sh`

#### Current Status
When trying to authenticate with Kerberos using `sqlplus /@XE` sqlplus returns the error:
```txt
ERROR:
ORA-01017: invalid username/password; logon denied
```

Looking at the kerberos logs we see the authentication transaction take place:
```sh
# Oracle user was authenticated and a the AS_REQ was issued
Mar 23 21:35:22 99364b92d0d9 krb5kdc[28](info): AS_REQ (8 etypes {18 17 20 19 16 23 25 26}) 10.5.0.11: NEEDED_PREAUTH: XE/oracle@EXAMPLE.COM for krbtgt/EXAMPLE.COM@EXAMPLE.COM, Additional pre-authentication required
Mar 23 21:35:22 99364b92d0d9 krb5kdc[28](info): AS_REQ (8 etypes {18 17 20 19 16 23 25 26}) 10.5.0.11: ISSUE: authtime 1584999322, etypes {rep=18 tkt=18 ses=18}, XE/oracle@EXAMPLE.COM for krbtgt/EXAMPLE.COM@EXAMPLE.COM
# A request for the TGS came through, and was issued
Mar 23 21:35:40 99364b92d0d9 krb5kdc[28](info): TGS_REQ (8 etypes {18 17 20 19 16 23 25 26}) 10.5.0.11: ISSUE: authtime 1584999322, etypes {rep=18 tkt=18 ses=18}, XE/oracle@EXAMPLE.COM for XE/oracle@EXAMPLE.COM
Mar 23 21:35:40 99364b92d0d9 krb5kdc[28](info): TGS_REQ (1 etypes {18}) 10.5.0.11: ISSUE: authtime 1584999322, etypes {rep=18 tkt=18 ses=18}, XE/oracle@EXAMPLE.COM for krbtgt/EXAMPLE.COM@EXAMPLE.COM
```

Then on the oracle side we get the following error output (After 2 minutes):
```sh
oracle_1    | ***********************************************************************
oracle_1    |
oracle_1    | Fatal NI connect error 12170.
oracle_1    |
oracle_1    |   VERSION INFORMATION:
oracle_1    | 	TNS for Linux: Version 18.0.0.0.0 - Production
oracle_1    | 	Oracle Bequeath NT Protocol Adapter for Linux: Version 18.0.0.0.0 - Production
oracle_1    | 	TCP/IP NT Protocol Adapter for Linux: Version 18.0.0.0.0 - Production
oracle_1    |   Version 18.4.0.0.0
oracle_1    |   Time: 23-MAR-2020 21:37:40
oracle_1    |   Tracing not turned on.
oracle_1    |   Tns error struct:
oracle_1    |     ns main err code: 12535
oracle_1    |
oracle_1    | TNS-12535: TNS:operation timed out
oracle_1    |     ns secondary err code: 12606
oracle_1    |     nt main err code: 0
oracle_1    |     nt secondary err code: 0
oracle_1    |     nt OS err code: 0
oracle_1    |   Client address: (ADDRESS=(PROTOCOL=tcp)(HOST=127.0.0.1)(PORT=35334))
oracle_1    | 2020-03-23T21:37:40.003997+00:00
oracle_1    | WARNING: inbound connection timed out (ORA-3136)
```
### Kerberos

Access Kerberos admin tooling
```sh
docker exec -it was-kerberos-database_kerberos_1 /bin/sh -c kadmin.local
```

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
[Configure Kerberos in Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/20/dbseg/configuring-kerberos-authentication.html#GUID-39A6604D-35DD-40E5-A71E-079EE7C9DF15)