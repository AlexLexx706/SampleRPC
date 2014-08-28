# -*- coding: utf-8 -*-
from tcp_rpc.client import Client
import logging 

logger = logging.getLogger(__name__)

class SensorsClient(Client):
    def __init__(self, host, port):
        Client.__init__(self, host, port)
    
    def ik_set_angle(self, angle):
        return self.send_cmd("ik_set_angle", angle)

    def ik_get_angle(self):
        return self.send_cmd("ik_get_angle")

    def ik_get_max_angle(self):
        return self.send_cmd("ik_get_max_angle")

    def ik_get_distance(self):
        return self.send_cmd("ik_get_distance")

    def ik_get_sector(self, count):
        return self.send_cmd("ik_get_sector", (count,))
        
    def us_get_distance(self):
        return self.send_cmd("us_get_distance")

    def get_marker_state(self):
        return self.send_cmd("get_marker_state")

    def get_data(self):
        return self.send_cmd("get_data")

        
def test(dt):
    start = time.time()

    while (time.time() - start) > dt:
        client.us_get_distance()
    
if __name__ == "__main__":
    import time
    client = SensorsClient('192.168.10.245', 8000)
    import cProfile
    
    
    start = time.time()
    count = 0

    while 1:
        client.get_data()
        count += 1
        dt = time.time() - start 

        if dt > 3:
            print "fps:", count / dt
            count = 0
            start = time.time()
