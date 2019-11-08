FROM ibmcom/websphere-traditional
ENV ENABLE_BASIC_LOGGING=true
COPY --chown=was:root tmp/PASSWORD /tmp/PASSWORD
COPY --chown=was:root docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]