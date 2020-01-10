FROM ibmcom/websphere-traditional
ENV ENABLE_BASIC_LOGGING=true
COPY --chown=was:root tmp/PASSWORD /tmp/PASSWORD
COPY --chown=was:root docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

USER root

RUN apt-get update
RUN apt-get install -y krb5-user libpam-krb5 libpam-ccreds auth-client-config
RUN chmod 777 /etc
RUN mkdir /etc/krb5
RUN printf 'add_entry -password -p db2user/db2@EXAMPLE.COM -k 1 -e aes256-cts\npassword\nwkt /etc/krb5.keytab' | ktutil


ENTRYPOINT ["/docker-entrypoint.sh"]