from value_player_widget import *
from laby_widget import * 

#déclare une application par défaut
path = "share/laby/levels/"
laby = labyrinth("share/laby/levels/0.laby")
view = View(laby)
player=ValuePlayerWidget(view)




#Créer notre Laby grace a la fonction Laby appelée depuis l'utilisateur.
#Le string s attendu est uniquement le numéro ou nom précis du niveau.
def Laby(s):
    global laby
    global view
    global player

    laby = labyrinth(path+s+".laby")
    view = View(deepcopy(laby))
    player=ValuePlayerWidget(view)
    return player

    

#Définition des fonctions pouvant être appelées par l'utilisateur.
def debut():
    player.debut()
    
def avance():
    player.avance()
    
def droite():
    player.droite()
    
def gauche():
    player.gauche()
    
def pose():
    player.pose()
    
def prend():
    player.prend()
    
def ouvre():
    player.ouvre()

def regarde():
    player.regarde()
    
def win():
    player.win()
    




