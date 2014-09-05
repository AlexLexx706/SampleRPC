#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import msgpack
import struct 
import logging

logger = logging.getLogger(__name__)

class Client:
    class ProtocolException(Exception):
        pass

    class Method:
        def __init__(self, client, name):
            self.client = client
            self.name = name
        def __call__(self, *args):
            return self.client.send_cmd(self.name, *args)

    def __init__(self, host, port=None):
        if port is None:
            if isinstance(host, str):
                host = host.replace("http://", "")
                host = host.replace("https://", "")

                params = host.split(":")
                self.host = params[0]
                self.port = int(params[1])
            else:
                self.host = host[0]
                self.port = int(host[1])
        else:
            self.host = host
            self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
    
    def read(self, size):
        res_buffer = ""
        while len(res_buffer) < size:
            res_buffer += self.sock.recv(size - len(res_buffer))
        return res_buffer

    def send_cmd(self, cmd, *data):
        buffer = msgpack.packb((cmd, data), use_bin_type=True)
        buffer = struct.pack("<L", len(buffer)) + buffer
        self.sock.sendall(buffer)
        size = struct.unpack("<L", self.read(4))[0]
        
        res = msgpack.unpackb(self.read(size), encoding='utf-8')
        
        if res[0] != 0:
            raise self.ProtocolException(res[1])
        return res[1]
    
    def __getattr__(self, name):
        return self.Method(self, name)

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
        