#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import msgpack
import struct 

class Client:
    class ProtocolException(Exception):
        pass
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
    
    def read(self, size):
        res_buffer = ""
        while len(res_buffer) < size:
            res_buffer += self.sock.recv(size - len(res_buffer))
        return res_buffer

    def send_cmd(self, cmd, data=()):
        buffer = msgpack.packb((cmd, data))
        buffer = struct.pack("<H", len(buffer)) + buffer
        self.sock.sendall(buffer)
        size = struct.unpack("<H", self.read(2))[0]
        res = msgpack.unpackb(self.read(size))
        
        if res[0] != 0:
            raise self.ProtocolException(res[1])
        return res[1]
    
    def close(self):
        self.sock.close()

if __name__ == "__main__":
    import sys
    import time
    
    c = Client("192.168.77.21", 8000)
    
    st = time.time()
    timeout = 4
    count = 0
    
    while 1:
        c.send_cmd(0, [1,2,3,4])
        dt =  time.time() - st
        count += 1;
        
        if dt > timeout:
            print "fps:", count/dt
            st = time.time()
            count = 0
        