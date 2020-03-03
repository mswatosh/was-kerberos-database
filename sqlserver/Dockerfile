FROM mcr.microsoft.com/mssql/server:2019-latest

USER root

RUN apt-get update
RUN apt-get install -y krb5-user libpam-krb5 libpam-ccreds auth-client-config
RUN chmod 777 /etc
RUN mkdir /etc/krb5
RUN printf 'add_entry -password -p db2user/db2@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil
RUN printf 'add_entry -password -p db2user/websphere@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil
RUN printf 'add_entry -password -p sqluser/sqlserver@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil
RUN printf 'add_entry -password -p MSSQLSvc/sqlserver:1433@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil

#RUN kinit -k -t /etc/krb5.keytab sqluser/sqlserver@EXAMPLE.COM
RUN /opt/mssql/bin/mssql-conf set network.disablesssd true
RUN /opt/mssql/bin/mssql-conf set network.enablekdcfromkrb5conf true
RUN /opt/mssql/bin/mssql-conf set network.privilegedadaccount sqluser
RUN /opt/mssql/bin/mssql-conf set network.kerberoskeytabfile /etc/krb5.keytab

ENV ACCEPT_EULA=Y
ENV MSSQL_SA_PASSWORD=P@ssw0rd

ADD docker-entrypoint.sh /
RUN chmod a+x /docker-entrypoint.sh

RUN mkdir /usr/src/app
COPY /usr/src/app/createschema.sh /usr/src/app/createschema.sh
RUN chmod a+x /usr/src/app/createschema.sh
COPY /usr/src/app/setup.sql /usr/src/app/setup.sql
RUN chmod a+x /usr/src/app/setup.sql

ENTRYPOINT ["/docker-entrypoint.sh"]