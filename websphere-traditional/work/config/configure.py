#Update hostname to websphere
AdminConfig.modify('(cells/DefaultCell01/nodes/DefaultNode01|serverindex.xml#ServerIndex_1)',  "[[hostName websphere]]")
AdminConfig.save()

#Enable App security
AdminTask.applyWizardSettings('[-secureApps true -secureLocalResources false -adminPassword password -userRegistryType WIMUserRegistry -adminName wsadmin ]')  
AdminConfig.save()


#Configure Kerberos
AdminTask.createKrbAuthMechanism('[-krb5Realm EXAMPLE.COM -krb5Config /etc/krb5.conf -krb5Keytab /etc/krb5.keytab -serviceName wassrvc -trimUserName true -enabledGssCredDelegate true -allowKrbAuthForCsiInbound true -allowKrbAuthForCsiOutbound true ]') 
AdminTask.setAdminActiveSecuritySettings('[-customProperties ["com.ibm.websphere.security.krb.useBuiltInMappingToSAF=false","com.ibm.websphere.security.krb.useRACMAPMappingToSAF=false"]]') 
AdminConfig.save()


#Setup JDBC Provider - DB2 XA Datasource
#jdbcProvider = AdminTask.createJDBCProvider('[-scope Node=DefaultNode01,Server=server1 -databaseType DB2 -providerType "DB2 Universal JDBC Driver Provider" -implementationType "XA data source" -name "DB2 Universal JDBC Driver Provider (XA)" -description "Two-phase commit DB2 JCC provider that supports JDBC 3.0. Data sources that use this provider support the use of XA to perform 2-phase commit processing. Use of driver type 2 on the application server for z/OS is not supported for data sources created under this provider." -classpath [/opt/drivers/db2jcc.jar] -nativePath [${DB2_JCC_DRIVER_NATIVEPATH} ] ]') 
jdbcProvider = AdminTask.createJDBCProvider('[-scope Cell=DefaultCell01 -databaseType DB2 -providerType "DB2 Using IBM JCC Driver" -implementationType "XA data source" -name "DB2 Using IBM JCC Driver (XA)" -description "Two-phase commit DB2 JCC provider that supports JDBC 4.0 using the IBM Data Server Driver for JDBC and SQLJ. IBM Data Server Driver is the next generation of the DB2 Universal JCC driver. Data sources created under this provider support the use of XA to perform 2-phase commit processing. Use of JDBC driver type 2 on WebSphere Application Server for Z/OS is not supported for data sources created under this provider. This provider is configurable in version 7.0 and later nodes." -classpath [/opt/drivers/db2jcc.jar ] -nativePath [${DB2_JCC_DRIVER_NATIVEPATH} ] ]')


#Configure Datasource
AdminTask.createAuthDataEntry('[-alias userpass -user dbuser@EXAMPLE.COM -password password -description ]') 
providerID = AdminTask.createJDBCProvider('[-scope Cell=DefaultCell01 -databaseType DB2 -providerType "DB2 Using IBM JCC Driver" -implementationType "Connection pool data source" -name "DB2 Using IBM JCC Driver" -description "One-phase commit DB2 JCC provider that supports JDBC 4.0 using the IBM Data Server Driver for JDBC and SQLJ. IBM Data Server Driver is the next generation of the DB2 Universal JCC driver. Data sources created under this provider support only 1-phase commit processing except in the case where JDBC driver type 2 is used under WebSphere Application Server for Z/OS. On WebSphere Application Server for Z/OS, JDBC driver type 2 uses RRS and supports 2-phase commit processing. This provider is configurable in version 7.0 and later nodes." -classpath [/opt/drivers/db2jcc.jar ] -nativePath [${DB2_JCC_DRIVER_NATIVEPATH} ] ]') 
AdminConfig.save()
datasourceID = AdminTask.createDatasource(jdbcProvider, '[-name DB2 -jndiName jdbc/krb5ds -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias -configureResourceProperties [[databaseName java.lang.String TESTDB] [driverType java.lang.Integer 4] [serverName java.lang.String db2] [portNumber java.lang.Integer 50000]]]') 
AdminTask.createDatasource(providerID, '[-name NoKrb5 -jndiName jdbc/nokrb5 -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence false -componentManagedAuthenticationAlias DefaultNode01/userpass -configureResourceProperties [[databaseName java.lang.String TESTDB] [driverType java.lang.Integer 4] [serverName java.lang.String db2] [portNumber java.lang.Integer 50000]]]') 
AdminConfig.create('MappingModule', datasourceID, '[[authDataAlias ""] [mappingConfigAlias KerberosMapping]]') 
custProps = AdminConfig.showAttribute(datasourceID, 'propertySet')
#AdminConfig.create('J2EEResourceProperty', custProps, '[[name "Krb5RecoveryPrincipal"] [type "java.lang.String"] [description ""] [value "dbuser@EXAMPLE.COM"] [required "false"]]')
#AdminConfig.create('J2EEResourceProperty', custProps, '[[name "Krb5RecoveryKeytab"] [type "java.lang.String"] [description ""] [value "{keytab}"] [required "false"]]'.format(keytab = "/etc/krb5.keytab"))
AdminConfig.save()


#Setup jdbc/db2krbkeytab - kerberos datasource with principal and keytab
db2krbkeytab = AdminTask.createDatasource(jdbcProvider, "[-name {name} -jndiName jdbc/{name} -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias -configureResourceProperties [[databaseName java.lang.String {dbname}] [driverType java.lang.Integer 4] [serverName java.lang.String {host}] [portNumber java.lang.Integer {port}]]]".format(name = "db2krbkeytab", dbname = "TESTDB", host = "db2", port = "50000"))
pool = AdminConfig.showAttribute(db2krbkeytab,'connectionPool')
AdminConfig.modify(pool, '[[connectionTimeout "10"] [maxConnections "2"] [unusedTimeout "1800"] [minConnections "0"] [agedTimeout "0"] [purgePolicy "EntirePool"] [reapTime "180"]]')

custProps = AdminConfig.showAttribute(db2krbkeytab, 'propertySet')
#AdminConfig.create('J2EEResourceProperty', custProps, '[[name "Krb5RecoveryPrincipal"] [type "java.lang.String"] [description ""] [value "dbuser@EXAMPLE.COM"] [required "false"]]')
#AdminConfig.create('J2EEResourceProperty', custProps, '[[name "Krb5RecoveryKeytab"] [type "java.lang.String"] [description ""] [value "{keytab}"] [required "false"]]'.format(keytab = "/etc/krb5.keytab"))
AdminConfig.create('MappingModule', db2krbkeytab, '[[authDataAlias ""] [mappingConfigAlias KerberosMapping]]') 

#Setup jdbc/db2krbcc - kerberos datasource with principal and credential cache
db2krbcc = AdminTask.createDatasource(jdbcProvider, "[-name {name} -jndiName jdbc/{name} -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias -configureResourceProperties [[databaseName java.lang.String {dbname}] [driverType java.lang.Integer 4] [serverName java.lang.String {host}] [portNumber java.lang.Integer {port}]]]".format(name = "db2krbcc", dbname = "TESTDB", host = "db2", port = "50000"))
pool = AdminConfig.showAttribute(db2krbcc,'connectionPool')
AdminConfig.modify(pool, '[[connectionTimeout "10"] [maxConnections "2"] [unusedTimeout "1800"] [minConnections "0"] [agedTimeout "0"] [purgePolicy "EntirePool"] [reapTime "180"]]')

custProps = AdminConfig.showAttribute(db2krbcc, 'propertySet')
#AdminConfig.create('J2EEResourceProperty', custProps, '[[name "Krb5RecoveryPrincipal"] [type "java.lang.String"] [description ""] [value "dbuser@EXAMPLE.COM"] [required "false"]]')
#AdminConfig.create('J2EEResourceProperty', custProps, '[[name "Krb5RecoveryCCache"] [type "java.lang.String"] [description ""] [value "{cc}"] [required "false"]]'.format(cc = "/tmp/krb5cc_1000"))
AdminConfig.create('MappingModule', db2krbcc, '[[authDataAlias ""] [mappingConfigAlias KerberosMapping]]') 

#Setup jdbc/db2nokrb - Non-kerberos datasource 
dbauth = AdminTask.createAuthDataEntry("[-alias db2Auth -user {user} -password {password} -description ]".format(user = "dbuser", password = "password"))
db2nokrb = AdminTask.createDatasource(jdbcProvider, '[-name {name} -jndiName jdbc/{name} -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias DefaultNode01/{authalias} -xaRecoveryAuthAlias DefaultNode01/{authalias} -configureResourceProperties [[databaseName java.lang.String {dbname}] [driverType java.lang.Integer 4] [serverName java.lang.String {host}] [portNumber java.lang.Integer {port}]]]'.format(name = "db2nokrb", authalias = "db2Auth", dbname = "TESTDB", host = "db2", port = "50000"))
pool = AdminConfig.showAttribute(db2nokrb,'connectionPool')
AdminConfig.modify(pool, '[[connectionTimeout "10"] [maxConnections "2"] [unusedTimeout "1800"] [minConnections "0"] [agedTimeout "0"] [purgePolicy "EntirePool"] [reapTime "180"]]')


#Set properties on Datasource
propSet = AdminConfig.showAttribute(datasourceID, 'propertySet')
myrps = AdminConfig.list('J2EEResourceProperty', propSet).split(lineSeparator)
for myrp in myrps: 
  myrpname = AdminConfig.showAttribute(myrp,"name")
  if myrpname=="kerberosServerPrincipal": 
    myrp = myrp[myrp.find("("):len(myrp)] 
    AdminConfig.modify(myrp, '[[name "kerberosServerPrincipal"] [type "java.lang.String"] [description "For a data source that uses Kerberos security, specifies the name that is used for the data source when it is registered with the Kerberos Key Distribution Center (KDC). It should be of the format user@realm."] [value "db2srvc@EXAMPLE.COM"] [required "false"]]')
  if myrpname=="securityMechanism":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]')
  if myrpname=="traceFile":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "traceFile"] [type "java.lang.String"] [description "The trace file to store the trace output. If you specify the trace file, the DB2 Jcc trace will be logged in this trace file. If this property is not specified and the WAS.database trace group is enabled, then both WebSphere trace and DB2 trace will be logged into the WebSphere trace file."] [value "/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/jcctrace.log"] [required "false"]]') 
  #if myrpname=="webSphereDefaultIsolationLevel":
  #  myrp = myrp[myrp.find("("):len(myrp)]
  #  AdminConfig.modify(myrp, '[[name "webSphereDefaultIsolationLevel"] [type "java.lang.Integer"] [description "Specifies a default transaction isolation level for new connections. Resource References and Access Intents override this value. To configure a default transaction isolation level, use the constants defined by JDBC: 1 (READ UNCOMMITTED), 2 (READ COMMITTED), 4 (REPEATABLE READ), 8 (SERIALIZABLE)."] [value "2"] [required "false"]]')
  if myrpname=="krb5RecoveryPrincipal":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "krb5RecoveryPrincipal"] [type "java.lang.String"] [description ""] [value "dbuser@EXAMPLE.COM"] [required "false"]]')
  if myrpname=="krb5RecoveryKeytab":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "krb5RecoveryKeytab"] [type "java.lang.String"] [description ""] [value "/etc/krb5.keytab"] [required "false"]]')
    #AdminConfig.remove(myrp)
  if myrpname=="krb5RecoveryCCache":
    myrp = myrp[myrp.find("("):len(myrp)]
    #AdminConfig.modify(myrp, '[[name "krb5RecoveryCCache"] [type "java.lang.String"] [description ""] [value "FILE:/tmp/krb5.ccache"] [required "false"]]')
    AdminConfig.remove(myrp)
AdminConfig.save()

#Set properties on Datasource keytab

propSet = AdminConfig.showAttribute(db2krbkeytab, 'propertySet')
myrps = AdminConfig.list('J2EEResourceProperty', propSet).split(lineSeparator)
for myrp in myrps: 
  myrpname = AdminConfig.showAttribute(myrp,"name")
  if myrpname=="kerberosServerPrincipal": 
    myrp = myrp[myrp.find("("):len(myrp)] 
    AdminConfig.modify(myrp, '[[name "kerberosServerPrincipal"] [type "java.lang.String"] [description "For a data source that uses Kerberos security, specifies the name that is used for the data source when it is registered with the Kerberos Key Distribution Center (KDC). It should be of the format user@realm."] [value "db2srvc@EXAMPLE.COM"] [required "false"]]')
  if myrpname=="securityMechanism":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]')
  if myrpname=="traceFile":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "traceFile"] [type "java.lang.String"] [description "The trace file to store the trace output. If you specify the trace file, the DB2 Jcc trace will be logged in this trace file. If this property is not specified and the WAS.database trace group is enabled, then both WebSphere trace and DB2 trace will be logged into the WebSphere trace file."] [value "/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/jcctrace.log"] [required "false"]]') 
  if myrpname=="traceFile":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "webSphereDefaultIsolationLevel"] [type "java.lang.Integer"] [description "Specifies a default transaction isolation level for new connections. Resource References and Access Intents override this value. To configure a default transaction isolation level, use the constants defined by JDBC: 1 (READ UNCOMMITTED), 2 (READ COMMITTED), 4 (REPEATABLE READ), 8 (SERIALIZABLE)."] [value "2"] [required "false"]]')
AdminConfig.save()

#Set properties on Datasource cc
propSet = AdminConfig.showAttribute(db2krbcc, 'propertySet')
myrps = AdminConfig.list('J2EEResourceProperty', propSet).split(lineSeparator)
for myrp in myrps: 
  myrpname = AdminConfig.showAttribute(myrp,"name")
  if myrpname=="kerberosServerPrincipal": 
    myrp = myrp[myrp.find("("):len(myrp)] 
    AdminConfig.modify(myrp, '[[name "kerberosServerPrincipal"] [type "java.lang.String"] [description "For a data source that uses Kerberos security, specifies the name that is used for the data source when it is registered with the Kerberos Key Distribution Center (KDC). It should be of the format user@realm."] [value "db2srvc@EXAMPLE.COM"] [required "false"]]')
  if myrpname=="securityMechanism":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]')
  if myrpname=="traceFile":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "traceFile"] [type "java.lang.String"] [description "The trace file to store the trace output. If you specify the trace file, the DB2 Jcc trace will be logged in this trace file. If this property is not specified and the WAS.database trace group is enabled, then both WebSphere trace and DB2 trace will be logged into the WebSphere trace file."] [value "/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/jcctrace.log"] [required "false"]]') 
  if myrpname=="traceFile":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "webSphereDefaultIsolationLevel"] [type "java.lang.Integer"] [description "Specifies a default transaction isolation level for new connections. Resource References and Access Intents override this value. To configure a default transaction isolation level, use the constants defined by JDBC: 1 (READ UNCOMMITTED), 2 (READ COMMITTED), 4 (REPEATABLE READ), 8 (SERIALIZABLE)."] [value "2"] [required "false"]]')
AdminConfig.save()

#Set Trace
serverName = "server1"
print serverName
server = AdminConfig.getid('/Server:'+serverName+'/')
print server
tc = AdminConfig.list('TraceService', server)
print tc
traceSpec = "*=info:WAS.database=all : WAS.j2c=all: RRA=all"# :com.ibm.ws.security.*=all:com.ibm.websphere.security.*=all"
print traceSpec
attrs = [["startupTraceSpecification", traceSpec]]
print attrs
AdminConfig.modify(tc, attrs)
AdminConfig.save()