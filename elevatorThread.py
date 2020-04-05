#!/usr/bin/python3
from Building import Building
import threading
import time 
class elevatorThread(threading.Thread):
    def __init__(self,building):
        threading.Thread.__init__(self)
        self.building=building
        
    def run(self):
        for elev in self.building.elevators:
            newUsers = self.building.getIntoElevator(elev.floor)
            leavers = elev.loadsUsers(newUsers)
            for user in leavers:
                self.building.arrivedAt(user, elev.floor)
                if(elev.floor != 1):
                    self.building.users[str(elev.floor)].append(user)
        time.sleep(10)
        for elev in self.building.elevators:
            elev.move(self.building.proposeFloor()) 