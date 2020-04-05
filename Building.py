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
        while True : 
            for elev in self.building.elevators:
                newUsers = self.building.getIntoElevator(elev.floor)
                leavers = elev.loadUsers(newUsers)
                for user in leavers:
                    self.building.arrivedAt(user, elev.floor)
                    if(elev.floor != 1):
                        self.building.users[str(elev.floor)].append(user)
                        for elev in self.building.elevators:
                            elev.idle = False
            time.sleep(10)
            for elev in self.building.elevators:
                elev.move(self.building.proposeFloor())

class userThread(threading.Thread):
    def __init__(self,building):
        threading.Thread.__init__(self)
        self.building=building
    
    def run(self):
        while True : 
            newUsers = self.building.generateUser()
            for user in newUsers:
                if(user.floorWanted not in self.building.calls):
                    self.building.calls.append(1)
            self.building.users['1'] += newUsers
            if self.building.totalTravels != 0 :
                self.building.meanWaitingTime = self.building.totalWaitingTime / self.building.totalTravels
            self.building.totalUsers += len(newUsers)
            for floor in self.building.users.values():
                for user in floor:
                    self.building.getBackHome(user)
            #affichage
            print("Etage            ",self.building.elevators[0].floor," Nb utilisateurs dans building : ", self.building.totalUsers)
            print("-------------------------------------------")
            print("List utilisateur ",self.building.elevators[0].users)
            
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
            newElevator = Elevator(False,False,[],2,FCFS)
            self.elevators.append(newElevator)

        userT = userThread(self)
        userT.start()

        elevatorT = elevatorThread(self)
        elevatorT.start()

    def generateUser(self):
        prob = numpy.random.poisson(0.5)
        users = []
        if prob != 0 :
            for i in range(prob):
                user = User(numpy.random.randint(2,8),time.time(),0,self.exp.rvs())
                users.append(user)
        return users
        
    
    def proposeFloor(self):
        if(len(self.calls) ==0 ):
            return -1
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
            if(user.floorWanted not in self.calls):
                self.calls.append(user.floorWanted)
                for elev in self.elevators:
                    elev.idle = False
            user.floorWanted = 1
            user.working = False

    def getIntoElevator(self, floor):
        inTransit = []
        for user in self.users[str(floor)]:
            if(not user.working):
                inTransit.append(user)
                self.users[str(floor)].remove(user)
        return inTransit

duil = Building(1)        