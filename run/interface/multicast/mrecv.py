#!/usr/bin/env python
import socket
import binascii

def main():
    HOST = "172.17.0.2"
    PORT = 81
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((HOST, PORT))

    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.error:
            print('Exception')
        finally:
            hexdata = binascii.hexlify(data)
            print ('Data = %s' % hexdata)
            print ('Str = %s' % str(data, encoding='utf-8'))

if __name__ == '__main__':
    main()
