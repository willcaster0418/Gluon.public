#!/bin/bash
if ! [ $# -eq 1 ]; then
    instance_name="gluon_instance"
else
    instance_name=$1
fi
docker cp ./pkg $instance_name:/install/