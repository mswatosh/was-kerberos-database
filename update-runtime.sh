#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "update-runtime.sh requires 1 argument, pointing to a jar file"
    exit 2
fi

if [[ $1 != *.jar ]]; then
	echo "Runtime replacement must be a jar file"
	exit 2
fi

if [ ! -f $1 ]; then
	echo "$1 does not exist"
	exit 2
fi



echo "Stopping WebSphere container"
docker stop was-kerberos-database_websphere_1
echo "Updating WebSphere runtime"
docker cp $1 was-kerberos-database_websphere_1:/opt/IBM/WebSphere/AppServer/plugins/com.ibm.ws.runtime.jar
echo "Starting WebSphere container"
docker start was-kerberos-database_websphere_1