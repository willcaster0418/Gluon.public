#!/bin/bash
source ~/.bashrc
ps aux|egrep uwsgi|egrep -v grep|awk '{print $2}'|xargs -Ix kill -9 x
ps aux|egrep python|egrep -v grep|awk '{print $2}'|xargs -Ix kill -9 x