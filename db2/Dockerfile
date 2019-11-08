FROM ibmcom/db2

RUN yum update -y
RUN yum -y install krb5-workstation krb5-libs krb5-auth-dialog

ADD docker-entrypoint.sh /
RUN chmod a+x /docker-entrypoint.sh

ENV LICENSE=accept
ENV DB2INSTANCE=username
ENV DB2INST1_PASSWORD=password
ENV DBNAME=testdb
ENV AUTOCONFIG=false
ENV ARCHIVE_LOGS=false

ENTRYPOINT ["/docker-entrypoint.sh"]