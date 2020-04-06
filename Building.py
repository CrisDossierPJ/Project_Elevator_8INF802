#!/usr/bin/python3
from User import User
from elevator import Elevator
from scipy.stats import poisson,exponnorm
import time
import numpy
import threading
from prettytable import PrettyTable
from os import system, name 
  
class userThread(threading.Thread):
    def __init__(self,building):
        threading.Thread.__init__(self)
        self.building=building
        
    def display(self):
        disp = PrettyTable()
        asc=[]
        for y in range(len(self.building.elevators)):
            ascenseur = [" "," "," "," "," "," "," "]
            asc.append(ascenseur)
        
        nbUser = [0,0,0,0,0,0,0]
        nbEtage = [1,2,3,4,5,6,7]
        i=0
        j=0
        nbUtilisateursActuel = 0
        
        for key, value in self.building.users.items():
            nbEtage[i] = str(key)
            nbUser[i] = len(value)
            nbUtilisateursActuel += len(value)
            i +=1
        disp.clear()
        disp.add_column("Numéro Etage",nbEtage)
        for ascenseur in asc:
            for i in range(len(ascenseur)):
                ascenseur[i] = " "
            ascenseur[self.building.elevators[j].floor - 1] = " X "
            nbUtilisateursActuel += len(self.building.elevators[j].users)
            j+=1
            disp.add_column("Ascenseur numero %s "%j,ascenseur)
                
        disp.add_column("Nombre de travailleurs dans l'étage",nbUser)
        
        
        '''
                    a = 0
            for b in self.building.users.values():
                a += len(b)
            a += len(self.building.elevators[0].users)
            print("Etage            ",self.building.elevators[0].floor," Nb utilisateurs total : ", self.building.totalUsers, "Nb users actuels : ",a)
            print("-------------------------------------------")
            print("List utilisateur ",self.building.elevators[0].users)
        '''
        print("Il y a un total de ",self.building.totalUsers," utilisateurs qui sont entrés dans le bâtiment")
        print("Il y a actuellement ",nbUtilisateursActuel,"utilisateur dans le batiment")
        print(disp)
        
    def clear(self): 
        system('cls')
    
    def run(self):
        userCooldown = 6
        while True : 
            if(userCooldown == 6):
                userCooldown = 0
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

            for elev in self.building.elevators:
                newUsers = self.building.getIntoElevator(elev.floor)
                leavers = elev.loadUsers(newUsers)
                for user in leavers:
                    self.building.arrivedAt(user, elev.floor)
                    if(elev.floor != 1):
                        self.building.users[str(elev.floor)].append(user)
                        for elev in self.building.elevators:
                            elev.idle = False
                for elev in self.building.elevators:
                    elev.move(self.building.proposeFloor())

            #affichage
            time.sleep(0.11)
            self.clear()
            self.display()
            userCooldown += 1
            
            
            

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