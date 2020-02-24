FROM open-liberty

USER root

RUN apt-get update
RUN apt-get install -y krb5-user libpam-krb5 libpam-ccreds auth-client-config
RUN chmod 777 /etc
RUN mkdir /etc/krb5
RUN printf 'add_entry -password -p db2user/db2@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil

ADD docker-entrypoint.sh /
RUN chmod a+x /docker-entrypoint.sh

#Copy new liberty image
#RUN rm /liberty/lib/com.ibm.ws.jdbc_1.0.33.jar
#COPY /updates /liberty

COPY server.xml /opt/ol/wlp/usr/servers/defaultServer/server.xml
COPY ./build/libs/was-kerberos-database.war /opt/ol/wlp/usr/servers/defaultServer/apps/was-kerberos-database.war
COPY ./build/dependencies/db2jcc.jar /opt/ol/wlp/usr/shared/db2jcc.jar
COPY ./build/libs/krb5LoginModule.jar /opt/ol/wlp/usr/shared/krb5LoginModule.jar
COPY jaas.conf /kerberos/jaas.conf

RUN echo "security.provider.1=com.ibm.crypto.provider.IBMJCE" >> /opt/ibm/java/jre/lib/security/java.security
RUN echo "security.provider.2=com.ibm.security.jgss.IBMJGSSProvider" >> /opt/ibm/java/jre/lib/security/java.security
RUN echo "login.config.url.1=file:/kerberos/jaas.conf" >> /opt/ibm/java/jre/lib/security/java.security

ENTRYPOINT ["/docker-entrypoint.sh"]