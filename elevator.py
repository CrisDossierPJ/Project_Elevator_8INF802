#!/usr/bin/python3
from User import User
import time
class Elevator:
    #idle :Boolean /pour savoir si l'ascenseur est au ralenti ou non
    #up :Boolean /  Nombres de places dans l'ascenseur
    #users : List<User> /  les clients présent dans l'ascenseur
    #floor : INT/ pour savoir ou est l'asenceur
    
    def __init__(self,idle,up,users,floor):
        self.idle = idle
        self.up = up
        self.users = users
        self.floor = floor

    #Fonction de prochain mouvement, appel fait par thread dans Building toutes les 10 secondes
    #proposedFloor : INT / de base à -1, sinon
    def move(self, proposedFloor = -1):

        #Si on a aucun Users, et que Building ne nous demande pas d'en récupérer, passage en mode Idle
        if(len(self.users) == 0 and proposedFloor == -1):
            self.idle = True
            #Pour le moment le mode idle ne fait rien,
            #l'ascenseur reste la ou il est.
            #Plus tard, ajouter un nouveau comportement pour comparer (ex : aller à l'étage 4)
            return

        #Sinon, priorité aux Users à l'intérieur
        nextFloor = -1
        if(len(self.users) != 0):
            #Choisir l'étage desiré selon la fonction choisie (First Come First Serve ou SSTF)

            #Pour le moment, juste FirstCome
            nextFloor = self.FirstComeFirstServe()
            #nextFloor = self.ShortestSeekTimeFirst()

        #Sinon prend le proposedFloor
        elif(len(self.users) == 0 and proposedFloor != -1):
            nextFloor = proposedFloor

        #Selon la valeur de nextFloor, on se deplace
        if(nextFloor > self.floor):
            self.up = True
            self.floor += 1
        else:
            self.up = False
            self.floor -= 1
        

    #Retourne l'etage du 1er User, ne prend pas en compte le sens actuel de déplacement
    def FirstComeFirstServe(self):
        return self.users[0].floorWanted

    
    #Retourne l'étage le plus intéressant selon les Users, et l'étage actuel
    def ShortestSeekTimeFirst(self):
        min = 0
        SeekFloor = -1
        for user in self.users:
            res = self.floor - user.floorWanted
            if res < 0:
                res * -1
            if res < min:
                min = res
                SeekFloor = user.floorWanted
            if min < 0:
                min * -1
        return SeekFloor
        pass

    #Retourne un étage selon la directino actuelle, et les Users actuels
    def LinearScan(self):
        #Voir pour l'étage le plus proche où des utilisateurs veulent descendre selon le sens actuel ????
        pass
    
    #----- 02/04/2020 cricri ---
    #Ajout d'un user dans l'ascsenceur
    def call(self,user):
        self.users.append(user)
        
    #Fonction a appelé après le move() et les 10 secondes, avant le prochain move
    #pour récupérer les Users à l'étage actuel.
    def loadUsers(self, newUsers = None):
        #Vider les Users arrivés à leur étage
        #en retournant une liste d'utilisateurs a Building
        leavers = []
        for user in self.users:
            if(user.floorWanted == self.floor):
                user.currentFloor = user.floorWanted
                leavers.append(user)
                   
        self.users = [x for x in self.users if x not in leavers]

        #Recupérer les nouveaux Users
        if newUsers != None:
            self.users += newUsers
        #Retourne les Users qui descendent
        return leavers
    
    #floorWanted : int / ou veut aller l'utilisateur ? 
    #begin/end : date/ heure d'arrivée / de sortie
    #workingTime : int / nb minutes passées dans le batiment
    #working : Boolean / L'utilisateur travaille ou non 
#Ils viennent d'arriver au premier etage
begin = time.time()
currentFloor = 1
us = User(2,begin,0,12,False,currentFloor)
uss = User(5,begin,0,13,False,currentFloor)
usf = User(4,begin,0,2,False,currentFloor)
usd = User(6,begin,0,3,False,currentFloor)


    #idle : Boolean /pour savoir si l'ascenseur est au ralenti ou non
    #up :Boolean /  Nombres de places dans l'ascenseur
    #users : List<User> /  les clients présent dans l'ascenseur
    #floor : INT/ pour savoir ou est l'asenceur
luser = []
luser.append(us)
luser.append(uss)
luser.append(usd)
luser.append(usf)


el = Elevator(True,False,[],5)
i = 0
workers = []
el.move(1)
el.loadUsers(luser)
while True:
    print(el.floor)
    el.move()
    time.sleep(1)
    workers += el.loadUsers()
    
    for worker in workers:
        worker.working = True
    
    
    i+=1
    if i ==10:
        print("Hey")
        for worker in workers:
            end = time.time()
            worker.goHome()
            
            el.move(worker.currentFloor)
            time.sleep(1)
            worker.end = end
            el.loadUsers(workers)
            
            print(worker.currentFloor)
            
            

            

