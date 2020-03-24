FROM open-liberty
USER root

# Update and install Kerberos (client head) and depenedency apps
RUN apt-get update
RUN apt-get install -y krb5-user libpam-krb5 libpam-ccreds auth-client-config

# Make excutable
RUN chmod 777 /etc
RUN mkdir /etc/krb5
RUN printf 'add_entry -password -p XE/oracle@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil

# Add startup script
ADD docker-entrypoint.sh /
RUN chmod a+x /docker-entrypoint.sh

# Copy server.xml, application, and jdbc driver
COPY oracle.server.xml /opt/ol/wlp/usr/servers/defaultServer/server.xml
COPY ./build/libs/was-kerberos-database.war /opt/ol/wlp/usr/servers/defaultServer/apps/was-kerberos-database.war
COPY ./build/dependencies/ojdbc8_g.jar /opt/ol/wlp/usr/shared/ojdbc8_g.jar

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]