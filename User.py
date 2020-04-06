#!/usr/bin/python3
import argparse
class User:
    #floorWanted : int / ou veut aller l'utilisateur ? 
    #begin/end : date/ heure d'arrivée / de sortie
    #workingTime : int / nb minutes passées dans le batiment
    #working : Boolean / L'utilisateur travaille ou non 
    def __init__(self,floorWanted,begin,end,workingTime,working = False):
        self.floorWanted = floorWanted
        self.begin = begin
        self.end = end
        self.workingTime = workingTime
        self.working = working
        

