FROM mcr.microsoft.com/mssql/server:2019-latest

USER root

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