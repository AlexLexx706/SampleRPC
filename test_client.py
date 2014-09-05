#!/usr/bin/python
# -*- coding: utf-8 -*-
from tcp_rpc.client import Client
import sys
import time

st = time.time()
timeout = 1
count = 0
data = " " *  8000

while 1:
    #c = Client("localhost", 8000)
    #c = Client(("localhost", 8000))
    #c = Client("localhost:8000")
    c = Client("https://localhost:8000")
    c.dummy(data)
    c.close()
    dt =  time.time() - st
    count += 1;
    
    if dt > timeout:
        print "fps:", count/dt
        st = time.time()
        count = 0