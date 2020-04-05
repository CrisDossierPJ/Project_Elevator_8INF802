#!/usr/bin/python3
from User import User
from scipy.stats import poisson,exponnorm
import time
import numpy

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
    
    def generateUser(self):
        prob = numpy.random.poisson(0.5)
        users = []
        if prob != 0 :
            for i in range(prob):
                user = User(numpy.random.randint(2,8),time.time(),0,self.exp.rvs())
                users.append(user)
        return users
        
    
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
        else:
            pass
    
