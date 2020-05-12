from enum import Enum
from functools import partial 
from collections import namedtuple
import re
from collections import namedtuple
import ipywidgets as widgets
import os
import math
from IPython.display import display
from ipywidgets import HBox, VBox
from IPython.display import Image
import random

#Class position 
class position :
    def __init__(self,i=0,j=0):
        self.i=i
        self.j=j
    def __eq__(self,other):
        return ( self.i == other.i ) and ( self.j == other.j )
    
    def __ne__(self,other):
        return not(self==other)
      
    


#class direction qui permet facielemtn de faire tourner la fourmi
direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast

        
#class board 
#définit le tableau de jeu, est un tableau de tuile
class  Board: 
    
    #constructeur
    def __init__(self,niveau):
        self.plateau=niveau
    
    #getter 
    def get(self,position):
        if (position.i<0 or position.j<0 or position.i >= len(self.plateau)or position.j>=len(self.plateau[0])):
            return Tiles.Outside
        else:
            return self.plateau[position.i][position.j] 
    
    #setter
    def set(self,position,tuile):
        if (position.i<0 or position.j<0 or position.i >= len(self.plateau)or position.j>=len(self.plateau[0])):
             print('erreur !!')   
        self.plateau[position.i][position.j]=tuile       

#remplis un tableau avec le board, la direction de la fourmi et sa position
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
            for tuiles in x: 
                if (tuiles=="←"):
                    stockI=i
                    stockJ=j
                    dire="3"
                    tuiles="."
                if (tuiles=="↓"):
                    stockI=i
                    stockJ=j
                    dire="2"
                    tuiles="."
                if (tuiles=="↑"): 
                    stockI=i
                    stockJ=j
                    dire="0"
                    tuiles="."
                if (tuiles =="→"):
                    stockI=i
                    stockJ=j
                    dire="1"
                    tuiles="."
                bleau.append(Tiles.char2Tile[tuiles])
                j+=1
            tab.append(bleau)
            i+=1
    return [tab,stockI,stockJ,dire]

#class Labyrinthe
#prend en paramètre notre string 
class labyrinth:
    
    #constructeur
    def __init__(self,s):
        
        self._won = False
        self.carry = Tiles.Void
        self.temp = charger(s)
        self.direction = self.temp[3]
        self.board = Board(self.temp[0])
        self.randomize()
        self.position = position(self.temp[1],self.temp[2])
        self.message = ""

    #initialise notre vue a partir du board
    def view(self):
        view = self.board
        size=self.size()
        if ( self.position.i < size[0] and
             self.position.j < size[1] ):
            view.plateau[self.position.i][self.position.j] = self.dirToAnt()
        return view
    
    #les 3 méthodes suivantes non pas été implémenter mais pourrait l'être pour un programme plus complet
    def to_string(self):
        pass

    def from_string(self):
        pass
    def html(self):
        pass    


    #Reset totalement notre labyrinthe a sa valeur initiale
    def reset(self): 
        self._won = False
        self.carry = Tiles.Void
        self.direction = self.temp[3]
        self.board = Board(self.temp[0])
        self.randomize()
        self.position = position(self.temp[1],self.temp[2])
        self.message = ""

    #renvoi la direction de notre fourmi
    def dirToAnt(self):
        if self.direction =="0":
            return Tiles.Ant_N
        elif self.direction =="1":
            return Tiles.Ant_E
        elif self.direction =="2":
            return Tiles.Ant_S
        elif self.direction =="3":
            return Tiles.Ant_W     
        
    #renvoi la taille du tableau
    def size(self):
        return (len(self.board.plateau),len(self.board.plateau[0]))
    
    #retourne la position de la case devant la fourmi
    def devant(self):
        return position(self.position.i+int(direction[self.direction][0]),self.position.j+int(direction[self.direction][1]))
        
    #tourne notre fourmi à gauche
    def gauche(self):
        self.direction = str((int(self.direction)-1)%4)
        self.message = ""
        return True
    
    #tourne notre fourmi à droite
    def droite(self):
        self.direction = str((int(self.direction)+1)%4)
        self.message = ""
        return True
    
    #fait avancer notre fourmi
    def avance(self):
        tile=self.board.get(self.position)
        tile_devant=self.board.get(self.devant())
        if(tile_devant==Tiles.Web or tile==Tiles.Exit or tile_devant==Tiles.Outside or tile_devant==Tiles.Exit
           or tile_devant==Tiles.Rock or tile_devant==Tiles.Wall):
            self.message = "je ne peux pas avancer."
            return False
        self.message = ""
        self.position = self.devant()
        return True
    
    #indique si l'on a gagné
    def win(self):
        self._won=True
        self.message="J'ai gagné !"
    
    def won(self):
        return self._won
    
    #Permet a notre fourmi de poser le caillou qu'elle porte
    def pose(self):
        if (self.carry==Tiles.Rock and (self.regarde()==Tiles.Void or self.regarde()==Tiles.Web 
                or self.regarde()==Tiles.SmallWeb or self.regarde()==Tiles.SmallRock  )):
            self.carry=Tiles.Void
            self.board.set(self.devant(),Tiles.Rock)
            self.message="J'ai posé ce que je portais"
            return True
        self.message="Je ne peux pas poser."
        return False
    
    #renvoi la tuile situé devant la fourmi
    def regarde(self):
        self.message=""
        return self.board.get(self.devant())
    
    #getter de psoition
    def get(self,pos):
        if ( pos == self.position ):
            return self.dirToAnt()
        else:
            return self.board.get(pos)
    
    #Ouvre la porte si la fourmi est devant
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
    
    #La fourmi va porter le caillou devant elel si il y en a un
    def prend(self):
        if (self.carry==Tiles.Void and self.regarde()==Tiles.Rock):
            self.carry=Tiles.Rock
            self.board.set(self.devant(),Tiles.Void)
            self.message="Je porte un objet"
            return True
        self.message = "Je ne peux pas prendre."
        return False

    #Permet de palcer aléatoirement les cailloux sur certaine carte qui le demandent 
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

#tuple de nos tuiles
Tile= namedtuple("Tile",["name","char"])

#class Tules représentant toutes nos tuiles psosible
class Tiles():
        Ant_E=Tile(name="ant-e",char="→")
        Ant_N=Tile(name="ant-n",char="↑")
        Ant_S=Tile(name="ant-s",char="↓")
        Ant_W=Tile(name="ant-w",char="←")
        Exit=Tile(name="exit",char="x")
        SmallRock=Tile(name="nrock",char="ŕ")
        SmallWeb=Tile(name="nweb",char="ẃ")
        Rock=Tile(name="rock",char="r")##declare ton appli 
        Void=Tile(name="void",char=".")
        Wall=Tile(name="wall",char="o")
        Web=Tile(name="web",char="w")
        Outside=Tile(name="void",char=" ")
        RandomRock=Tile(name="void",char="R")
        RandomWeb=Tile(name="void",char="W")
        
       
     #création de nos dictionnaires utiles par la suite   
Tiles.tile2Png=dict()        
Tiles.char2N=dict()
Tiles.char2Tile=dict()
for t in Tiles.__dict__.values():
    if isinstance(t, Tile):
        pof = t.name
        image = "include/laby/tiles_png/" + pof + ".png"
        file = open (image,'rb')
        image_lu = file.read()
        Tiles.tile2Png[t]=(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="inline-flex",
        width="32",height="32",border="15px"
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




    

