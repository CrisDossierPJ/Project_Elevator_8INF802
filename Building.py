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
    
    def generateUser(self):
        prob = numpy.random.poisson(0.5)
        rv = exponnorm(60)
        if prob != 0 :
            user = User(numpy.random.randint(2,8),time.time(),0,rv)
        else :
            return None
        return user
        
    
    def proposeFloor(self):
        return self.calls[0]

    
