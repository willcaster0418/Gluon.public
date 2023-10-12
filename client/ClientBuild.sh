#!/bin/bash
if ! [ $# -eq 1 ]; then
    instance_name="gluon_instance"
else
    instance_name=$1
fi
containerStatus=$(docker ps --filter name=$instance_name --format "{{.Status}}")
if ! [[ $containerStatus =~ "Up"* ]]; then
    docker start $instance_name
fi
docker exec -i $instance_name bash -c "rm -rf /client-dist/"

npm run build
docker cp ./build $instance_name:/client-dist
sleep 10