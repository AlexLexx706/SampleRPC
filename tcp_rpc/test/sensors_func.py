 # -*- coding: utf8 -*-
#!/usr/bin/python
from infrared_scaner import Scanner as IKScanner
from ultrasonic_scanner import Scanner as USScanner
from cross_detector.cross_detector import CrossDetector
from cross_detector.opencv_reader import OpencvReader
import time
import logging

logging.getLogger(__name__)

class MyFuncs:
    def __init__(self):
        try:
            logging.debug("->")

            self.c_detector = CrossDetector(False, reader=OpencvReader())
            self.ik_scanner = IKScanner(180)
            self.us_scanner = USScanner()
            self.c_detector.start()
            self.ik_scanner.start()
            self.us_scanner.start()
        finally:
            logging.debug("<-")
        
    
    def stop(self):
        try:
            logging.debug("->")

            self.c_detector.stop()
            self.ik_scanner.stop()
            self.us_scanner.stop()
        finally:
            logging.debug("<-")

    def ik_set_angle(self, angle):
        try:
            logging.debug("->")
            return self.ik_scanner.set_angle(angle)
        finally:
            logging.debug("<-")
    
    def ik_get_angle(self):
        try:
            logging.debug("->")
            return self.ik_scanner.get_angle()
        finally:
            logging.debug("<-")


    def ik_get_max_angle(self):
        try:
            logging.debug("->")
            return self.ik_scanner.get_max_angle()
        finally:
            logging.debug("<-")


    def ik_get_distance(self):
        try:
            logging.debug("->")
            return self.ik_scanner.get_distance()
        finally:
            logging.debug("<-")


    def ik_get_sector(self, count):
        try:
            logging.debug("->")
            return self.ik_scanner.get_sector(count)
        finally:
            logging.debug("<-")
        
    def us_get_distance(self):
        try:
            logging.debug("->")
            return self.us_scanner.get_distance()
        finally:
            logging.debug("<-")

    def get_marker_state(self):
        try:
            logging.debug("->")
            state = self.c_detector.get_marker_state() 
            logging.debug("marker_state:{}".format(state))
            return state
        finally:
            logging.debug("<-")