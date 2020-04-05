#!/usr/bin/python3
from Building import Building
import threading
import time 
class elevatorThread(threading.Thread):
    def __init__(self,building):
        threading.Thread.__init__(self)
        self.building=building
        
    def run(self):
        pass
        #TODO :  - LoadUser dans chaque Elevator 
        #       time.sleep(10)
        #       pour chaque ascenseur --> move(etage conseillé)  