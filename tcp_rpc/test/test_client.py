#!/usr/bin/python
# -*- coding: utf-8 -*-
from tcp_rpc.client import Client
import sys
import time

st = time.time()
timeout = 4
count = 0

while 1:
    c = Client("192.168.77.17", 8000)
    c.send_cmd("dummy")
    c.close()
    dt =  time.time() - st
    count += 1;
    
    if dt > timeout:
        print "fps:", count/dt
        st = time.time()
        count = 0