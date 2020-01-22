#Update hostname to websphere
AdminConfig.modify('(cells/DefaultCell01/nodes/DefaultNode01|serverindex.xml#ServerIndex_1)',  "[[hostName websphere]]")
AdminConfig.save()

#Disable Admin security
AdminTask.setGlobalSecurity ('[-enabled false]')
AdminConfig.save()

#Configure Kerberos
AdminTask.createKrbAuthMechanism('[-krb5Realm EXAMPLE.COM -krb5Config /etc/krb5.conf -krb5Keytab /etc/krb5.keytab -serviceName db2user -trimUserName true -enabledGssCredDelegate true -allowKrbAuthForCsiInbound true -allowKrbAuthForCsiOutbound true ]') 
AdminTask.setAdminActiveSecuritySettings('[-customProperties ["com.ibm.websphere.security.krb.useBuiltInMappingToSAF=false","com.ibm.websphere.security.krb.useRACMAPMappingToSAF=false"]]') 
AdminConfig.save()

#Configure Datasource
providerID = AdminTask.createJDBCProvider('[-scope Cell=DefaultCell01 -databaseType DB2 -providerType "DB2 Using IBM JCC Driver" -implementationType "Connection pool data source" -name "DB2 Using IBM JCC Driver" -description "One-phase commit DB2 JCC provider that supports JDBC 4.0 using the IBM Data Server Driver for JDBC and SQLJ. IBM Data Server Driver is the next generation of the DB2 Universal JCC driver. Data sources created under this provider support only 1-phase commit processing except in the case where JDBC driver type 2 is used under WebSphere Application Server for Z/OS. On WebSphere Application Server for Z/OS, JDBC driver type 2 uses RRS and supports 2-phase commit processing. This provider is configurable in version 7.0 and later nodes." -classpath [/opt/drivers/db2jcc.jar ] -nativePath [${DB2_JCC_DRIVER_NATIVEPATH} ] ]') 
AdminConfig.save()
datasourceID = AdminTask.createDatasource(providerID, '[-name DB2 -jndiName jdbc/db2ds -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias -configureResourceProperties [[databaseName java.lang.String TESTDB] [driverType java.lang.Integer 4] [serverName java.lang.String db2] [portNumber java.lang.Integer 50000]]]') 
AdminConfig.create('MappingModule', datasourceID, '[[authDataAlias ""] [mappingConfigAlias KerberosMapping]]') 
AdminConfig.save()