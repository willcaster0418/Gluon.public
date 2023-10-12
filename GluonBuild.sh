#!/bin/bash
if ! [ $# -eq 1 ]; then
    instance_name="gluon_instance"
else
    instance_name=$1
fi
containerStatus=$(docker ps --filter name=$instance_name --format "{{.Status}}")
if ! [[ $containerStatus =~ "Up"* ]]; then
    echo "### Starting container"
    docker start $instance_name
fi

echo "### Deleting files install"
docker exec -i $instance_name bash -c "rm -rf /install/"

echo "### Copying files to container"
docker cp ./install/ $instance_name:/
docker cp ./config $instance_name:/install/
docker cp ./run $instance_name:/install/
docker cp ./pkg $instance_name:/install/

echo "### redo install"
docker exec -i $instance_name bash -c "bash /install/install.sh"

echo "### re-Starting container"
docker stop $instance_name
docker start $instance_name

cd client
./ClientBuild.sh $instance_name

echo "### Done! exit for ctrl+c"

sleep 30