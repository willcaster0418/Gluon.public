#!/bin/bash
source ~/.bashrc
/gluon/run/stop.sh
sleep 1

rm -f /gluon/log/*
rm -f /dev/shm/*
touch /gluon/log/daily.log

service nginx start
service mariadb start
python3 /gluon/run/mw.py &

mysql -u root < /install/sql/system.sql
mysql -u root < /install/sql/oms.sql

python3 /gluon/run/batch/batch.py
python3 /gluon/run/snap/shared_write.py

python3 /gluon/run/daemon/FMS/RealTimeDaemon.py &
python3 /gluon/run/interface/market/naver.py &
python3 /gluon/run/interface/order/fake.py &

uwsgi --ini=/gluon/config/query.config     --chdir /gluon/run/daemon/FMS --enable-threads
uwsgi --ini=/gluon/config/orderbook.config --chdir /gluon/run/daemon/FMS --enable-threads
uwsgi --ini=/gluon/config/auth.config      --chdir /gluon/run/daemon/FMS --enable-threads
uwsgi --ini=/gluon/config/api.config       --chdir /gluon/run/daemon/FMS --enable-threads

/bin/bash