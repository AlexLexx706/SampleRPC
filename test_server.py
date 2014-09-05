#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
from tcp_rpc.server import ThreadedTCPServer

class Test:
    def dummy(self, data):
        return data

logging.basicConfig(level=100, format="%(asctime)s %(levelname)s proc:%(process)d %(filename)s::%(funcName)s %(message)s") 
#1. создали сервак
server = ThreadedTCPServer(("0.0.0.0", 8000), Test())

#2. запуск сервака
server.serve_forever()