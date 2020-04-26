# Project_Elevator_8INF802
Projet de simulation modélisant le fonctionnement d'ascenseurs réalisé dans le cadre du cours 8INF802:Simulation de systèmes.
Afin d'exécuter le projet, executer le fichier 'Building.py'

# Installer les dépendances

Via votre outil d'installation de librairies pour Python3 (pip3, anaconda, ...), veuillez installer les librairies suivantes:
 - scipy
 - numpy
 - prettytable
 - tkinter
 
Lorsque toutes les dépendances sont installés, vous pouvez lancez la simulation

# Lancer la simulation

Pour lancer la simulation, executez le fichier Building.py de la sorte : 'python3 Building.py' (ou 'python Building.py' sous Windows). Executer la simulation de la sorte utilisera les valeurs par defaut des différents arguments.

Pour obtenir la liste des arguments modifiables dans votre console, lancez : 'python3 Building.py -h'


Liste des arguments : 

 - "--nbAscenseur" : Int definissant le nombre d'ascenseurs pour la simulation (defaut : 2)
 
 - "--typeAlgorithme" : String, choix de l'algorithme de déplacement des ascenseurs 
    - "FCFS" : First Come First Serve
    - "SSTF" : Shortest Seek Time First

 - "--lamb" : Float, valeur de lambda pour la génération d'utilisateurs suivant une loi Poisson (défaut : 0.5)
 
 - "--expo" : Int, valeur pour la loi exponentielle génerant le temps de travail d'un utilisateur (défaut : 60)
 
 - "--typeIdle" : String, choix entre les 4 types d'Idle pour les ascenseurs:
    - "movingIdle" : se rend au 4e etage
    - "noMoveIdle" : reste au dernier etage atteint
    - "goDownIdle" : se rend à l'étage inférieur
    - "goUpIdle" : se rend à l'étage supérieur



Pour quitter la simulation a tout moment, appuyez sur la touche 'Echap'.
Lorsque la simulation est quittée, un fichier .csv avec les données de la simulation est géneré.

