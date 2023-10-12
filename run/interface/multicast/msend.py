#!/usr/bin/env python
import socket, time, sys
'''
Ethernet adapter vEthernet (WSL):
   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::a193:dd6c:a9d6:c8b4%51
   IPv4 Address. . . . . . . . . . . : 172.19.32.1
   Subnet Mask . . . . . . . . . . . : 255.255.240.0
   Default Gateway . . . . . . . . . :

def main():
  MCAST_GRP = '172.19.32.1'
  MCAST_PORT = 3001
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.sendto(bytes('Hello World!', encoding='utf-8'), (MCAST_GRP, MCAST_PORT))
'''
def main():
  HOST = '172.19.32.1'
  PORT = 3001
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.sendto(bytes('Hello World!', encoding='utf-8'), (HOST, PORT))

if __name__ == '__main__':
  main()
