from value_player_widget import *
from laby_widget import * 

##declare ton appli 



laby = labyrinth("share/laby/levels/0.laby")
view = View(laby)
player=ValuePlayerWidget(view)





def Laby(s):
    global laby
    global view
    global player
    laby = labyrinth(s)
    view = View(copy(laby))
    player=ValuePlayerWidget(view)
    return player

    

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
    




