# was-kerberos-database

Admin Console: https://localhost:9043/ibm/console/  
User: wsadmin  
Password: password

srvcon_gssplugin_list
/opt/ibm/db2/V11.5/security64/plugin/IBM/server/IBMkrb5.so

/bin/su db2user -c "/opt/ibm/db2/V11.5/bin/db2 CONNECT TO testdb"


### Kerberos
Realm: EXAMPLE.COM
User: db2user/db2@EXAMPLE.COM

```
kinit admin/admin@EXAMPLE.COM  
su admin  
/opt/ibm/db2/V11.5/bin/db2 CATALOG DATABASE testdb AUTHENTICATION KERBEROS TARGET PRINCIPAL admin/admin@EXAMPLE.COM
```

```
ktutil -k krb5.keytab add -p db2user/admin@EXAMPLE.COM -w password -e aes256-cts-hmac-sha1-96 -V 1
```

```
/opt/ibm/db2/V11.5/adm/db2start
```
gss_acquire_cred: (851968,39756033) Unspecified GSS failure.  Minor code may provide more information.  No key table entry found for db2user/59cc7e8837ed@EXAMPLE.COM...0.........

```
/database/config/db2user/sqllib/db2dump/DIAG0000/
```

```
#/opt/ibm/db2/V11.5/bin/db2 CATALOG DATABASE testdb AUTHENTICATION KERBEROS TARGET PRINCIPAL db2user/db2@EXAMPLE.COM
```
### TODO
~~Add krb5 to each image~~ Remove from WAS ?  
[Configure Kerberos in WAS](https://www.ibm.com/support/knowledgecenter/en/SSEQTP_9.0.5/com.ibm.websphere.base.doc/ae/tsec_kerb_setup.html)  
[Configure Kerberos in DB2](https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.db2.luw.admin.sec.doc/doc/c0058525.html)