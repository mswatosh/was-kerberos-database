#AdminApp.install('/work/app/was-kerberos-database.war', '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -appname was-kerberos-database_war -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -noenableClientModule -clientMode isolated -novalidateSchema -contextroot /was-kerberos-database -MapResRefToEJB [[ was-kerberos-database.war "" was-kerberos-database.war,WEB-INF/web.xml jdbc/db2ds javax.sql.DataSource jdbc/db2ds "" "" "" ]] -MapModulesToServers [[ was-kerberos-database.war was-kerberos-database.war,WEB-INF/web.xml WebSphere:cell=DefaultCell01,node=DefaultNode01,server=server1 ]] -MapWebModToVH [[ was-kerberos-database.war was-kerberos-database.war,WEB-INF/web.xml default_host ]] -CtxRootForWebMod [[ was-kerberos-database.war was-kerberos-database.war,WEB-INF/web.xml /was-kerberos-database ]]]' ) 
AdminApp.install('/work/app/was-kerberos-database.war', '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -appname was-kerberos-database_war -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -noenableClientModule -clientMode isolated -novalidateSchema -contextroot /was-kerberos-database -MapResRefToEJB [[ was-kerberos-database.war "" was-kerberos-database.war,WEB-INF/web.xml jdbc/nokrb5 javax.sql.DataSource jdbc/nokrb5 "" "" "" ][ was-kerberos-database.war "" was-kerberos-database.war,WEB-INF/web.xml jdbc/db2ds javax.sql.DataSource jdbc/db2ds KerberosMapping "" "" ]] -MapModulesToServers [[ was-kerberos-database.war was-kerberos-database.war,WEB-INF/web.xml WebSphere:cell=DefaultCell01,node=DefaultNode01,server=server1 ]] -MapWebModToVH [[ was-kerberos-database.war was-kerberos-database.war,WEB-INF/web.xml default_host ]] -CtxRootForWebMod [[ was-kerberos-database.war was-kerberos-database.war,WEB-INF/web.xml /was-kerberos-database ]]]' ) 
#Update app for kerberos login
#AdminApp.edit('was-kerberos-database_war', '[ -MapResRefToEJB [[ was-kerberos-database.war "" was-kerberos-database.war,WEB-INF/web.xml jdbc/db2ds javax.sql.DataSource jdbc/db2ds KerberosMapping "" "" ]]]' ) 

#Map users
AdminTask.createUser('[-uid db2user/websphere -cn db2 -sn user -password password -confirmPassword password]')
AdminApp.edit('was-kerberos-database_war', '[ -MapRolesToUsers [[ Manager AppDeploymentOption.No AppDeploymentOption.No db2user/websphere "" AppDeploymentOption.No user:defaultWIMFileBasedRealm/uid=db2user/websphere,o=defaultWIMFileBasedRealm "" ]]]' )

AdminConfig.save()