FROM ibmcom/websphere-traditional
ENV ENABLE_BASIC_LOGGING=true

USER root
RUN yum update -y
RUN yum install -y krb5-workstation krb5-libs
RUN chmod 777 /etc
RUN mkdir /etc/krb5
RUN printf 'add_entry -password -p wassrvc/websphere@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil
RUN printf 'add_entry -password -p dbuser@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil

COPY --chown=was:root tmp/PASSWORD /tmp/PASSWORD
COPY --chown=was:root docker-entrypoint.sh /docker-entrypoint.sh
COPY --chown=was:root work/config/configure.py /work/config/configure.py
COPY --chown=was:root work/config/installApps.py /work/config/installApps.py
COPY --chown=was:root ./build/libs/was-kerberos-database.war /work/app/
RUN chmod a+x /docker-entrypoint.sh
#configure.py is run in docker-entrypoint.sh
RUN chmod a+x /work/config/configure.py 
RUN /work/configure.sh /work/config/installApps.py

COPY ./build/dependencies/db2jcc.jar /opt/drivers/db2jcc.jar


ENTRYPOINT ["/docker-entrypoint.sh"]