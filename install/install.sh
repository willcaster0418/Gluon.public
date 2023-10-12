#!/bin/bash
cp -f /install/.bashrc /root/.bashrc
source /root/.bashrc

mkdir -p /gluon/config
mkdir -p /gluon/log
mkdir -p /gluon/log/prev

rm -rf /gluon/run
rm -rf /gluon/pkg
rm -rf /gluon/config

cp -r /install/run /gluon/
cp -r /install/pkg /gluon/
cp -r /install/config /gluon/

rm /etc/nginx/conf.d/default.conf
ln -s /gluon/config/nginx-config /etc/nginx/conf.d/default.conf
