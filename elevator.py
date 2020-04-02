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

    
    #Retourne l'étage le plsu intéressant selon les Users, et l'étage actuel
    def ShortestSeekTimeFirst(self):
        pass

    #Retourne un étage selon la directino actuelle, et les Users actuels
    def LinearScan(self):
        #Voir pour l'étage le plus proche où des utilisateurs veulent descendre selon le sens actuel ????
        pass


    #Fonction a appelé après le move() et les 10 secondes, avant le prochain move
    #pour récupérer les Users à l'étage actuel.
    def loadUsers(self, newUsers):
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

    """
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
    """