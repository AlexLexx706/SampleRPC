#!/usr/bin/python
# -*- coding: utf-8 -*-
import SocketServer
import msgpack
import struct
import socket
import logging
import traceback

logger = logging.getLogger(__name__)

#потоковый сервер
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    class MyTCPHandler(SocketServer.BaseRequestHandler):
        def read(self, size):
            res_buffer = ""
            while len(res_buffer) < size:
                b = self.request.recv(size - len(res_buffer))
                if len(b) == 0:
                    raise socket.error("end connection")
                res_buffer += b
            return res_buffer
            
        def handle(self):
            try:
                logger.debug("handle(self:{}) ->".format(self))
                while 1:
                    try:
                        buffer = self.read(2)
                        size = struct.unpack("<H", buffer)[0]
                        cmd, params = msgpack.unpackb(self.read(size), encoding='utf-8')

                        if self.server.instance is None:
                            packet = msgpack.packb((1, params))
                        else:
                            try:
                                packet = msgpack.packb((0, getattr(self.server.instance, cmd)(*params)))
                            except:
                                result = traceback.format_exc()
                                logger.error(result)
                                packet = msgpack.packb((2, result))
                        self.request.sendall(struct.pack("<H", len(packet)) + packet)
                    except socket.error as e:
                        logger.error(e)
                        return
            finally:
                logger.debug("handle(self:{}) <-".format(self))
                
   
    def __init__(self, host, instance):
        SocketServer.TCPServer.__init__(self, host, self.MyTCPHandler)
        self.instance = instance
        

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=0, format="%(asctime)s %(levelname)s proc:%(process)d %(filename)s::%(funcName)s %(message)s") 
    
    if len(sys.argv) < 3:
        host = "0.0.0.0"
        port = 8000
        logging.info("using defauil host:{0} port:{1}".format(host, port))
    else:
        host, port = sys.argv[1:]
        logging.info("using host:{0} port:{1}".format(host, port))

    #1. создали сервак
    server = ThreadedTCPServer((host, int(port)), None)

    #2. запуск сервака
    server.serve_forever()