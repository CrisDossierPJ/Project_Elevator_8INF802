#!/usr/bin/python3
from User import User
from elevator import Elevator
from scipy.stats import poisson,exponnorm
import time
import numpy
import threading

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

class userThread(threading.Thread):
    def __init__(self,building):
        threading.Thread.__init__(self)
        self.building=building
    
    def run(self):
        newUsers = self.building.generateUser()
        for user in newUsers:
            if(user.wantedFloor not in self.building.calls):
                self.building.calls.append(user.wantedFloor)
        self.building.users['1'] += newUsers
        self.building.meanWaitingTime = self.building.totalWaitingTime / self.building.totalTravels
        self.building.totalUsers += len(newUsers)
        #affichage
        time.sleep(1)

class Building:
    #elevators : list<Elevator> /
    #users : dict<Int,User> 
    def __init__(self, nbElevator, FCFS = True):
        self.elevators = []
        self.users = {
            '1' : [],
            '2' : [],
            '3' : [],
            '4' : [],
            '5' : [],
            '6' : [],
            '7' : []
        }
        self.totalUsers = 0
        self.totalTravels = 0
        self.totalWaitingTime = 0
        self.meanWaitingTime = 0
        self.calls = []
        self.exp = exponnorm(60)

        for i in range(nbElevator):
            newElevator = Elevator(False,False,[],1,FCFS)
            self.elevators.append(newElevator)

        userT = userThread(self)
        userT.start()

        elevatorT = elevatorThread(self)
        elevatorT.start()

    def generateUser(self):
        prob = numpy.random.poisson(0.5)
        if prob != 0 :
            user = User(numpy.random.randint(2,8),time.time(),0,self.exp.rvs())
        else :
            return None
        return user
        
    
    def proposeFloor(self):
        return self.calls[0]


    def arrivedAt(self, user, floor):
        user.end = time.time()
        diff = user.end - user.begin
        self.totalWaitingTime += diff
        self.totalTravels += 1
        if(floor == 1):
            del user
        else:
            user.begin = 0
            user.working = True

    def getBackHome(self, user):
        if(user.end + user.workingTime >= time.time()):
            user.begin = time.time()
            user.end = 0
            if(user.wantedFloor not in self.calls):
                self.calls.append(user.wantedFloor)
            user.wantedFloor = 1
            user.working = False

    def getIntoElevator(self, floor):
        inTransit = []
        for user in self.users[floor]:
            if(not user.Working):
                inTransit.append(user)
                self.users[floor].remove(user)
        return inTransit

        