#!/usr/bin/python3

class Elevator:
    #up :Boolean /  Nombres de places dans l'ascenseur
    #idle :Boolean /pour savoir si l'ascenseur est au ralenti ou non
    #floor : INT/ pour savoir ou est l'asenceur
    #users : List<User> /  les clients present dans l'ascenseur
    def __init__(self,idle,up,users,floor, FCFS,typeIdle):
        self.idle = idle
        self.up = up
        self.users = users
        self.floor = floor
        self.FCFS = FCFS
        self.typeIdle = typeIdle

    #Fonction de prochain mouvement, appel fait par thread dans Building toutes les 10 secondes
    #proposedFloor : INT / de base a -1, sinon
    def move(self, proposedFloor = -1):

        #Si on a aucun Users, et que Building ne nous demande pas d'en recuperer, passage en mode Idle
        if(len(self.users) == 0 and proposedFloor == -1):
            self.idle = True
            #Pour le moment le mode idle ne fait rien,
            #l'ascenseur reste la ou il est.
            #Plus tard, ajouter un nouveau comportement pour comparer (ex : aller a l'etage 4)
            if self.typeIdle == "movingIdle": 
                proposedFloor = 4
            elif self.typeIdle == "goUpIdle":
                proposedFloor = self.floor +1
            elif self.typeIdle == "goDownIdle":
                proposedFloor = self.floor -1
            elif self.typeIdle == "noMoveIdle":
                return
                
                

        #Sinon, priorite aux Users a l'interieur
        nextFloor = -1
        if(len(self.users) != 0):
            #Choisir l'etage desire selon la fonction choisie (First Come First Serve ou SSTF)
            if(self.FCFS):
                nextFloor = self.FirstComeFirstServe()
            else:
                nextFloor = self.ShortestSeekTimeFirst()

        #Sinon prend le proposedFloor
        elif(len(self.users) == 0 and proposedFloor != -1):
            nextFloor = proposedFloor

        #Selon la valeur de nextFloor, on se deplace
        if nextFloor != -1:
            if(nextFloor == self.floor):
                return
            if(nextFloor > self.floor ):
                self.up = True
                self.floor += 1
            else:
                self.up = False
                self.floor -= 1
        

    #Retourne l'etage du 1er User, ne prend pas en compte le sens actuel de deplacement
    def FirstComeFirstServe(self):
        return self.users[0].floorWanted

    
    #Retourne l'etage le plus interessant selon les Users, et l'etage actuel
    def ShortestSeekTimeFirst(self):
        min = 0
        SeekFloor = 0
        for user in self.users:
            res = abs(self.floor - user.floorWanted)
            if min ==0:
                min = res
                SeekFloor = user.floorWanted
            if res < min:
                min = res
                SeekFloor = user.floorWanted
        return SeekFloor
        
    #Fonction a appele apres le move() et les 10 secondes, avant le prochain move
    #pour recuperer les Users a l'etage actuel.
    def loadUsers(self, newUsers = []):
        #Vider les Users arrives a leur etage
        #en retournant une liste d'utilisateurs a Building
        leavers = []
        for user in self.users:
            if(user.floorWanted == self.floor):
                leavers.append(user)
        self.users = [x for x in self.users if x not in leavers]

        #Recuperer les nouveaux Users
        self.users += newUsers

        #Retourne les Users qui descendent
        return leavers