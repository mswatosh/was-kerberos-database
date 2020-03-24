FROM oracle/database:18.4.0-xe

# Update and install Kerberos (server head)
RUN yum update -y
RUN yum -y install krb5-workstation krb5-libs krb5-auth-dialog

COPY setup/ /opt/oracle/scripts/setup
COPY startup/ /opt/oracle/scripts/startup

ENV ORACLE_PWD=password

RUN mkdir /etc/krb5
RUN printf 'add_entry -password -p XE/oracle@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil

RUN chmod a+x /opt/oracle/scripts/setup/1kerberos.sh
RUN chmod a+x /opt/oracle/scripts/setup/2oracle.sh
RUN chmod a+x /opt/oracle/scripts/setup/3kerberos.sh
RUN chmod a+x /opt/oracle/scripts/startup/oracle.sql