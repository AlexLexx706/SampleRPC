 # -*- coding: utf8 -*-
#!/usr/bin/python
import logging
import sys
#from sensors_func import MyFuncs
from dummy_func import MyFuncs
from tcp_rpc.server import ThreadedTCPServer

logging.basicConfig(level=0, format="%(asctime)s %(levelname)s proc:%(process)d %(filename)s::%(funcName)s %(message)s") 

if len(sys.argv) < 3:
    host = "0.0.0.0"
    port = 8000
    print "using defauil params host:{0} port:{1}".format(host, port)
else:
    host, port = sys.argv[1:]

#1. создали сервак
server = ThreadedTCPServer((host, int(port)), MyFuncs())

#2. запуск сервака
server.serve_forever()
