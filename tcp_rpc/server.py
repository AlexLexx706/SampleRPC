#!/usr/bin/python
# -*- coding: utf-8 -*-
import SocketServer
import msgpack
import struct
import socket
import logging
import traceback
import json

logger = logging.getLogger(__name__)

#потоковый сервер
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    class MyTCPHandler(SocketServer.BaseRequestHandler):
        class EndConnection(Exception): pass
        
        def read(self, size):
            res_buffer = ""
            while len(res_buffer) < size:
                b = self.request.recv(size - len(res_buffer))
                if len(b) == 0:
                    raise self.EndConnection()
                res_buffer += b
            return res_buffer
            
        def handle(self):
            try:
                logger.debug("(self:{}) ->".format(self))
                while 1:
                    try:
                        buffer = self.read(4)
                        size = struct.unpack("<L", buffer)[0]

                        try:
                            if self.server.serialization == "json":
                                cmd, params = json.loads(self.read(size))

                                if params is not None:
                                    packet = json.dumps(getattr(self.server.instance, cmd)(params))
                                else:
                                    packet = json.dumps(getattr(self.server.instance, cmd)())
                            else:
                                cmd, params = msgpack.unpackb(self.read(size), encoding='utf-8')
                                packet = msgpack.packb((0, getattr(self.server.instance, cmd)(*params)), use_bin_type=True)
                        except:
                            result = traceback.format_exc()
                            logger.error(result)
                            packet = msgpack.packb((2, result), use_bin_type=True)

                        self.request.sendall(struct.pack("<L", len(packet)) + packet)
                    except self.EndConnection:
                        return
                    except socket.error as e:
                        logger.error(e)
                        return
            finally:
                logger.debug("handle(self:{}) <-".format(self))
                
    def __init__(self, host, instance, serialization="msgpack"):
        #поставим ограничение подключений в 100000
        self.request_queue_size = 100000
        SocketServer.TCPServer.__init__(self, host, self.MyTCPHandler)
        self.instance = instance
        self.serialization=serialization
        

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