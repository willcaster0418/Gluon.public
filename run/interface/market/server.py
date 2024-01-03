import socket
import time
import sys

multicast_group = '224.1.1.1'
port = 7000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

time.sleep(1)
f=open("MKT_DATA.txt","rb")
while f:
    dataTosend=b''
    for i in range(20):
        data = f.readline()
        dataTosend += data
    sock.sendto(dataTosend,(multicast_group, port))
    time.sleep(0.3)

sock.close()