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
#props = AdminConfig.create('J2EEResourcePropertySet', datasourceID,[]) 
#AdminConfig.create('J2EEResourceProperty', props, '[[name "kerberosServerPrincipal"] [type "java.lang.String"] [description "For a data source that uses Kerberos security, specifies the name that is used for the data source when it is registered with the Kerberos Key Distribution Center (KDC). It should be of the format user@realm."] [value "db2user@EXAMPLE.COM"] [required "false"]]')
#AdminConfig.create('J2EEResourceProperty', props, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]') 
propSet = AdminConfig.showAttribute(datasourceID, 'propertySet')
#AdminConfig.create('J2EEResourceProperty', propSet, '[[name "kerberosServerPrincipal"] [type "java.lang.String"] [description "For a data source that uses Kerberos security, specifies the name that is used for the data source when it is registered with the Kerberos Key Distribution Center (KDC). It should be of the format user@realm."] [value "db2user@EXAMPLE.COM"] [required "false"]]') 
#AdminConfig.modify('J2EEResourceProperty', propSet, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]') 
#AdminConfig.modify(propSet, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]')

myrps = AdminConfig.list('J2EEResourceProperty', propSet).split(lineSeparator)
for myrp in myrps: 
  myrpname = AdminConfig.showAttribute(myrp,"name")
  if myrpname=="kerberosServerPrincipal": 
    myrp = myrp[myrp.find("("):len(myrp)] 
    AdminConfig.modify(myrp, '[[name "kerberosServerPrincipal"] [type "java.lang.String"] [description "For a data source that uses Kerberos security, specifies the name that is used for the data source when it is registered with the Kerberos Key Distribution Center (KDC). It should be of the format user@realm."] [value "db2user/websphere@EXAMPLE.COM "] [required "false"]]')
  if myrpname=="securityMechanism":
    myrp = myrp[myrp.find("("):len(myrp)]
    AdminConfig.modify(myrp, '[[name "securityMechanism"] [type "java.lang.Integer"] [description "Specifies the DRDA security mechanism. Possible values are: 3 (CLEAR_TEXT_PASSWORD_SECURITY), 4 (USER_ONLY_SECURITY), 7 (ENCRYPTED_PASSWORD_SECURITY), 9 (ENCRYPTED_USER_AND_PASSWORD_SECURITY), or 11 (KERBEROS_SECURITY). If this property is specified, the specified security mechanism is the only mechanism that is used. If no value is specified for this property, 3 is used."] [value "11"] [required "false"]]')
AdminConfig.save()

#Set Trace
serverName = "server1"
print serverName
server = AdminConfig.getid('/Server:'+serverName+'/')
print server
tc = AdminConfig.list('TraceService', server)
print tc
traceSpec = "*=info: WAS.j2c=all: RRA=all"
print traceSpec
attrs = [["startupTraceSpecification", traceSpec]]
print attrs
AdminConfig.modify(tc, attrs)
AdminConfig.save()