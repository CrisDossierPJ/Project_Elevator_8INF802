#!/usr/bin/python3

class Elevator:
    #up :Boolean /  Nombres de places dans l'ascenseur
    #idle :Boolean /pour savoir si l'ascenseur est au ralenti ou non
    #floor : INT/ pour savoir ou est l'asenceur
    #users : List<User> /  les clients présent dans l'ascenseur
    def __init__(self,idle,up,users,floor):
        self.idle = idle
        self.up = up
        self.users = users
        self.floor = floor
    
    #Premier arrivé premier servi
    def FirstComeFirstServe(self):
        if self.users.size() != 0:
            for i in range(0,self.users.size()):
                goTo(self.users(i).floorWanted)
                #wait(10)
                for i in range(0,self.users.size()):
                    if(self.floor == self.users(i).floorWanted):
                        self.users.remove(i)
        return 0
    def goTo(self,floorUser):
        self.floor = floorUser
        
    def shortestSeekTimeFirst(self):
        return 0
    def LinearScan(self):
        return 0