#!/usr/bin/python3

class Elevator:
    #up :Boolean /  Nombres de places dans l'ascenseur
    #idle :Boolean /pour savoir si l'ascenseur est au ralenti ou non
    #floor : INT/ pour savoir ou est l'asenceur
    #users : List<User> /  les clients présent dans l'ascenseur
    def __init__(self,idle,up,users,floor, FCFS):
        self.idle = idle
        self.up = up
        self.users = users
        self.floor = floor
        self.FCFS = FCFS

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
            if(self.FCFS):
                nextFloor = self.FirstComeFirstServe()
            else:
                nextFloor = self.ShortestSeekTimeFirst()

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
            res = abs(self.floor - user.floorWanted)
            if min ==0:
                min = res
            if res < min:
                min = res
                SeekFloor = user.floorWanted
        return SeekFloor
    
    #----- 02/04/2020 cricri ---
    #Ajout d'un user dans l'ascsenceur
    def boardUsers(self,user):
        self.users.append(user)
        
    #Fonction a appelé après le move() et les 10 secondes, avant le prochain move
    #pour récupérer les Users à l'étage actuel.
    def loadUsers(self, newUsers = []):
        #Vider les Users arrivés à leur étage
        #en retournant une liste d'utilisateurs a Building
        leavers = []
        for user in self.users:
            if(user.floorWanted == self.floor):
                leavers.append(user)
        self.users = [x for x in self.users if x not in leavers]

        #Recupérer les nouveaux Users
        self.users += newUsers

        #Retourne les Users qui descendent
        return leavers