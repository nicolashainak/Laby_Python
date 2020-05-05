from enum import Enum
from functools import partial 
from collections import namedtuple
import re
from collections import namedtuple
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# from PIL import Image 
import ipywidgets as widgets
import os
import math
from IPython.display import display
from ipywidgets import HBox, VBox
# import PIL
# import numpy as np
# import re
from IPython.display import Image
# from IPython.display import display
import random

class position :
    def __init__(self,i=0,j=0):
        self.i=i
        self.j=j
    def __eq__(self,other):
        return ( self.i == other.i ) and ( self.j == other.j )
    
    def __ne__(self,other):
        return not(self==other)
      
    

PlayDirection = Enum('PlayDirection','Forward Backward None')
direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast
class dimension(position):
    def __init__(self,i=0,j=0):
        position.__init__(self,i,j) 
        

class  Board: 
    def __init__(self,niveau):
        self.plateau=niveau
    def copy(self):
        return self
    def get(self,position):
        if (position.i<0 or position.j<0 or position.i >= len(self.plateau)or position.j>=len(self.plateau[0])):
            return Tiles.Outside
        else:
            return self.plateau[position.i][position.j] 
    
    def set(self,position,tuile):
        if (position.i<0 or position.j<0 or position.i >= len(self.plateau)or position.j>=len(self.plateau[0])):
             print('erreur !!')   
        self.plateau[position.i][position.j]=tuile       

def charger(nom_niveau):
    fichier = open(nom_niveau, 'r+')
    tab = []
    i=0
    j=0
    stockI=-1


    stockJ=-1
    dire=0
    for line in fichier:
        
        j=0
        bleau=[]
        if (len(line)>0 and (line[0] == "o" or line[0] =="." or line[0] =="x")):
            x = line.split()
            for nimportequoi in x: 
                if (nimportequoi=="←"):
                    stockI=i
                    stockJ=j
                    dire="3"
                    nimportequoi="."
                if (nimportequoi=="↓"):
                    stockI=i
                    stockJ=j
                    dire="2"
                    nimportequoi="."
                if (nimportequoi=="↑"): 
                    stockI=i
                    stockJ=j
                    dire="0"
                    nimportequoi="."
                if (nimportequoi =="→"):
                    stockI=i
                    stockJ=j
                    dire="1"
                    nimportequoi="."
                bleau.append(Tiles.char2Tile[nimportequoi])
                j+=1
            tab.append(bleau)
            i+=1
    return [tab,stockI,stockJ,dire]

class labyrinth:
    ## a rajouter from string // to string // html 
    
    def __init__(self,s):
        
        self._won = False
        self.carry = Tiles.Void
        self.temp = charger(s)
        self.direction = self.temp[3]
        self.board = Board(self.temp[0])
        self.randomize()
        self.position = position(self.temp[1],self.temp[2])
        self.message = ""

    def copy(self):
        return self

    def view(self):
        view = self.board
        size=self.size()
        if ( self.position.i < size[0] and
             self.position.j < size[1] ):
            # The ant is on the board; display it
            view.plateau[self.position.i][self.position.j] = self.dirToAnt()
        return view
    
    def to_string(self):
        pass

    def from_string(self):
        pass
    def html(self):
        pass    



    def reset(self): 
        self._won = False
        self.carry = Tiles.Void
        self.direction = self.temp[3]
        self.board = Board(self.temp[0])
        self.randomize()
        self.position = position(self.temp[1],self.temp[2])
        self.message = ""

    def dirToAnt(self):
        if self.direction =="0":
            return Tiles.Ant_N
        elif self.direction =="1":
            return Tiles.Ant_E
        elif self.direction =="2":
            return Tiles.Ant_S
        elif self.direction =="3":
            return Tiles.Ant_W     
        
    def size(self):
        return (len(self.board.plateau),len(self.board.plateau[0]))
    
    def devant(self):
        return position(self.position.i+int(direction[self.direction][0]),self.position.j+int(direction[self.direction][1]))
        
    
    def gauche(self):
        self.direction = str((int(self.direction)-1)%4)
        self.message = ""
        return True
    
    def droite(self):
        self.direction = str((int(self.direction)+1)%4)
        self.message = ""
        return True
    
    def avance(self):
        tile=self.board.get(self.position)
        tile_devant=self.board.get(self.devant())
        if(tile_devant==Tiles.Web or tile==Tiles.Exit or tile_devant==Tiles.Outside or tile_devant==Tiles.Exit
           or tile_devant==Tiles.Rock or tile_devant==Tiles.Wall):
            self.message = "je ne peux pas avancer."
            return False
        self.message = ""
        print("j'avance dans avance ")
        self.position = self.devant()
        return True
    
    def win(self):
        self._won=True
        self.message="J'ai gagné !"
    
    def won(self):
        return self._won
    
    def pose(self):
        if (self.carry==Tiles.Rock and (self.regarde()==Tiles.Void or self.regarde()==Tiles.Web 
                or self.regarde()==Tiles.SmallWeb or self.regarde()==Tiles.SmallRock  )):
            self.carry=Tiles.Void
            self.board.set(self.devant(),Tiles.Rock)
            self.message=""
            return True
        self.message="Je ne peux pas poser."
        return False
    
    def regarde(self):
        self.message=""
        return self.board.get(self.devant())
    
    def get(self,pos):
        if ( pos == self.position ):
            return self.dirToAnt()
        else:
            return self.board.get(pos)
    
    def ouvre(self):
        if self.regarde()!= Tiles.Exit :
            self.message = "Je ne peux pas ouvrir."
            return False
        if self.carry != Tiles.Void:
            self.message = "Je ne peux pas ouvrir en portant un objet."
            return False
        self.position = self.devant()
        self.win()
        return True
    
    def prend(self):
        if (self.carry==Tiles.Void and self.regarde()==Tiles.Rock):
            self.carry=Tiles.Rock
            self.board.set(self.devant(),Tiles.Void)
            self.message=""
            return True
        self.message = "Je ne peux pas prendre."
        return False
     
    def randomize(self):
        n_random_rocks=0
        n_random_webs=0
        for row in self.board.plateau:
            for c in row:
                if(c==Tiles.RandomRock):
                    n_random_rocks =n_random_rocks +1
                if(c==Tiles.RandomWeb):
                    n_random_webs =n_random_webs +1
        r_rock =math.floor( random.random()*25 % n_random_rocks) if n_random_rocks else 0
        r_web = math.floor( random.random()*25 % n_random_webs) if n_random_webs else 0
        n_random_rocks=0
        n_random_webs=0
        nRow=0
        
        for row in self.board.plateau:
            nC=0 
            for c in row:
                if (c == Tiles.RandomRock):
                    if (n_random_rocks == r_rock):
                         self.board.plateau[nRow][nC] = Tiles.SmallRock
                    else:
                        self.board.plateau[nRow][nC] = Tiles.Rock
                    n_random_rocks =n_random_rocks +1
                
                if (c == Tiles.RandomWeb):
                    if (n_random_webs == r_web):
                        self.board.plateau[nRow][nC] = Tiles.SmallWeb
                    else:
                        self.board.plateau[nRow][nC] = Tiles.Web
                    n_random_webs =n_random_webs +1
                nC=nC+1
               
            nRow=nRow+1  

Tile= namedtuple("Tile",["name","char"])

class Tiles():
        Ant_E=Tile(name="ant-e",char="→")
        Ant_N=Tile(name="ant-n",char="↑")
        Ant_S=Tile(name="ant-s",char="↓")
        Ant_W=Tile(name="ant-w",char="←")
        Exit=Tile(name="exit",char="x")
        SmallRock=Tile(name="nrock",char="ŕ")
        SmallWeb=Tile(name="nweb",char="ẃ")
        Rock=Tile(name="rock",char="r")
        Void=Tile(name="void",char=".")
        Wall=Tile(name="wall",char="o")
        Web=Tile(name="web",char="w")
        Outside=Tile(name="void",char=" ")
        RandomRock=Tile(name="void",char="R")
        RandomWeb=Tile(name="void",char="W")
        
       
        
Tiles.tile2Png=dict()        
Tiles.char2N=dict()
Tiles.char2Tile=dict()
for t in Tiles.__dict__.values():
    if isinstance(t, Tile):
        pof = t.name
        image = "include/laby/tiles_png/" + pof + ".png"
        file = open (image,'rb')
        image_lu = file.read()
        Tiles.tile2Png[t]=(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="flex",
        margin="1" ,padding="0", width="50%"
        )))
        Tiles.char2N[t.char]=t.name
        Tiles.char2Tile[t.char]=t
              

Tiles.char2T=dict()
p=re.compile('[A-Z]+(\w)*')
for t in Tiles.__dict__.keys() :
    z=p.match(t)
    if (z!=None):
        d=z.group()
        Tiles.char2T[getattr(Tiles,t).char]=d




def LabyrinthView(laby):
    carte = laby.board.plateau
    items=[]
    taille_ligne =0
    
    for j in range (0,len(carte)):
        taille_ligne = len(carte[0])
        for i in range (0,len(carte[0])):
            if(j==laby.position.i and i==laby.position.j):
                tuile= laby.dirToAnt()
            else:
                tuile = laby.board.get(position(j,i))
            
            pof = tuile.name
            image = "include/laby/tiles_png/" + pof + ".png"
            file = open (image,'rb')
            image_lu = file.read()
            items.append(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="flex",
            margin="1" ,padding="0", width="50%"
            )))
    return (items,taille_ligne)
    

#<<-- l = valeur de l'historique
# def LabyrinthView(laby):
#     carte = laby.board.plateau
#     items=[]
#     taille_ligne =0
    
#     for j in range (0,len(carte)):
#         taille_ligne = len(carte[0])
#         for i in range (0,len(carte[0])):
#             if(j==laby.position.i and i==laby.position.j):
#                 tuile= laby.dirToAnt()
#             else:
#                 tuile = l.board.get(position(j,i))
            
#             pof = tuile.name
#             image = "include/laby/tiles_png/" + pof + ".png"
#             file = open (image,'rb')
#             image_lu = file.read()
#             items.append(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="flex",
#             margin="1px", width="100%"
#             )))
#     display(widgets.GridBox(items,layout=widgets.Layout(grid_template_columns="repeat("+str(taille_ligne)+", 50px)")))



    
    