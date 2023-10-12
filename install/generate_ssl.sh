#!/bin/bash
SSL_PATH=/install/ssl
openssl ecparam -out $SSL_PATH/rootca.key -name prime256v1 -genkey
openssl req -new -sha256 -key $SSL_PATH/rootca.key -out $SSL_PATH/rootca.csr

openssl x509 -req -sha256 -days 999999 -in $SSL_PATH/rootca.csr -signkey $SSL_PATH/rootca.key -out $SSL_PATH/rootca.crt

openssl ecparam -out $SSL_PATH/server.key -name prime256v1 -genkey

openssl req -new -sha256 -key $SSL_PATH/server.key -out $SSL_PATH/server.csr

openssl x509 -req -sha256 -days 999999 -in $SSL_PATH/server.csr -CA $SSL_PATH/rootca.crt -CAkey $SSL_PATH/rootca.key -CAcreateserial -out $SSL_PATH/server.crt

# openssl x509 -in server.crt -text -noout

cat $SSL_PATH/server.crt $SSL_PATH/rootca.crt > $SSL_PATH/server.pem