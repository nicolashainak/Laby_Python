from enum import Enum
import ipywidgets
from functools import partial 
from ipywidgets import HBox, VBox ,GridBox ,Layout
from threading import *
from timer import *
from traits.api import Delegate, HasTraits, Instance,Int, Str
from traitlets import *
from laby_widget import *
from copy import *


#class enum qui décrit les type de direction possible
PlayDirection = Enum('PlayDirection','Forward Backward None')

#Class Player (qui hérite de HasTraits):
# argument : visualisation
# -> Créer un player qui va gerer l'historique de notre widget 
# -> attends des valeur via la méthode set_value(x) a mettre dans l'historique   

class Player(HasTraits) :
        time=Int()

        #lance notre timer 
        def run(self):
            self.timer.run()
        
        #Méthode de mise a jour 
        def update(self):
            self.slider_time.value=self.time
            self.view.value = self.history[self.time]
            self.view.update()
            

        #recupère la dernière valeur de l'historique
        def get_value(self):
            return self.history[len(self.history)-1]
        
        #Ajoute une valeur à l'historique
        def set_value(self,value): 
            if (len(self.history) > 1000):
                raise RuntimeError("Votre programme a pris plus de 1000 étapes")
            self.history.append(value)
            self.slider_time.max=len(self.history)-1
            if ( not self.timer.running() and self.time == len(self.history) -2):
                self.time=self.time+1
                self.update()
        
        #appel la fonction correspondante au sens de lecture
        def tick(self):
            if(self.play_direction == PlayDirection.Forward ):  
                self.step_forward()
            else:
                self.step_backward()
        
        #Relance le niveau
        def reset(self,value):      
                self.time=0
                self.history=[(value)]
                self.slider_time.max=len(self.history)-1
                self.update()
        
        #Se déplace à la première valeur de l'historique 
        def begin(self):
            self.time=0
            self.update()
        
        #Se déplace à la dernière valeur de l'historique 
        def end(self):
            self.time= len(self.history)-1  
            self.update()

        #Recul d'une étape
        def step_backward(self):
            if( self.time >0):
                self.time=self.time-1
                self.update()

        #avance d'une étape
        def step_forward(self):
            if( self.time <len(self.history)-1):  
                self.time=self.time+1
                self.update()  

        #permet de repartir en arrière 
        def backward (self):
            self.play_direction = PlayDirection.Backward 
            self.timer.set_fps(self.play_fps)
        
        #relance le timer 
        def play(self):
            self. play_direction = PlayDirection.Forward 
            self.timer.set_fps(self.play_fps)
            self.timer.run()

        #met en pause le temps
        def pause(self):
            self.play_direction=None
            self.timer.cancel()
            
        
        #définit la vitesse de rafraichissement
        def set_fps(self,fps):
            self.play_fps=fps
            if(self.play_direction != None):
                self.timer.set_fps(fps)
        
        #renvoie si l'on a gagné
        def won(self):
            return self.history[len(self.history)-1].won()
        
        #change la valeur du temps actuel 
        def set_time(self,tps):  
            self.time=tps
            
        #constructeur
        def __init__(self, _view):
            self.view = _view
            self.original_value=deepcopy(self.view.value)
            self.play_direction=PlayDirection.Forward
            self.play_fps=1
            self.timer =PerpetualTimer( self.play_fps,self.tick )
            self.history=[(self.view.value)]
            self.time=0
           
            
            #créer le slider de temps
            self.slider_time=ipywidgets.IntSlider(
                value=self.time,
                min=0,
                max=0,#len(self.history),
                step=1,
                description="time:"
            )
            self.reset(deepcopy(self.original_value))
                
            #modifie le time en observant le slider.
            def on_value_change(change):
                self.time=change['new']
            #associe l'observe et le slider
            self.slider_time.observe(on_value_change,names='value')
            



#Class PlayerView ( qui hérite de VBox):
# argument : Player
# -> Créer un PlayerView qui va gerer l'affichage et va activer les méthodes du player et de notre modèle  

class PlayerView(VBox):

    #l'ensemble des méthodes suivantes (avant le constructeur )sont appelées par global_fr et par l'utilisateur et 
    # appelle les méthodes correspondantes de notre modèle mais sur une copie a chaque fois afin d'avoir des valeur diffèrente dans l'historique
    def set_value(self,value):
        self.player.set_value(value)
    
    def debut(self):
        self.player.view.value.reset()

    def avance(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.avance()
        self.set_value(mycopy)
         
    def droite(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.droite()
        self.set_value(mycopy)
          
    def gauche(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.gauche()
        self.set_value(mycopy)

    def pose(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.pose()
        self.set_value(mycopy)      

    def prend(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.prend()
        self.set_value(mycopy)

    def ouvre(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.ouvre()
        self.set_value(mycopy)

    def regarde(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.regarde()
        self.set_value(mycopy)
        
    def win(self):
        mycopy = deepcopy(self.player.history[len(self.player.history)-1])
        mycopy.win()
        self.set_value(mycopy)
    

    #Constructeur
    def __init__(self,player):
        
        self.widget=ipywidgets.HTML(
        value="",
        placeholder='',
        description='',
        )
        output = ipywidgets.Output()
        self.player=player
        
        # les méthodes suivantes définissent les actions réaliser par les boutons correspondants
        def fast_backward_clicked(b):
            with output:
                self.player.begin()
                self.player.pause()
            
        def backward_clicked(b):
            with output:
                self.player.backward()
        def step_backward_clicked(b):
            with output: 
                self.player.pause()
                self.player.step_backward()
        def pause_clicked(b):
            with output:
                self.player.pause()
        def step_forward_clicked(b):
            with output:
                self.player.pause()
                self.player.step_forward()

        def play_clicked(b):
            with output:
                self.player.play()
        def fast_forward_clicked(b):
            with output:
                self.player.pause()
                self.player.end()
                            
    
        
        #créer un slider de vitesse
        slider=ipywidgets.FloatSlider(
        value=1.0,
        min=0.0,
        max=6.0,
        step=1,
            description="Speed:"
        )
        #observe le changement du slider vitesse et appel set_fps
        def on_value_change(change):
            value=int (change['new'])
            self.player.set_fps(2**value)
        
        #création des boutons du widget et liaison des méthodes et des boutons
        slider.observe(on_value_change, names='value')

        play= ipywidgets.Button(description="",icon='fa-play',layout=Layout(width='35px'))
        fast_backward= ipywidgets.Button(description="",icon='fa-fast-backward',layout=Layout(width='35px'))
        backward= ipywidgets.Button(description="",icon='fa-backward',layout=Layout(width='35px'))
        step_backward= ipywidgets.Button(description="",icon='fa-step-backward',layout=Layout(width='35px'))
        pause= ipywidgets.Button(description="",icon='fa-pause',layout=Layout(width='35px'))
        step_forward= ipywidgets.Button(description="",icon='fa-step-forward',layout=Layout(width='35px'))
        fast_forward= ipywidgets.Button(description="",icon='fa-fast-forward',layout=Layout(width='35px'))

        play.on_click(play_clicked)
        fast_backward.on_click(fast_backward_clicked)
        backward.on_click(backward_clicked)
        step_backward.on_click(step_backward_clicked)
        pause.on_click(pause_clicked)
        step_forward.on_click(step_forward_clicked)
        fast_forward.on_click(fast_forward_clicked)

        
        
        self.player=player
        self.player.reset(self.player.view.value)
        #méthode qui gère le message afficher
        def fctOut(slid_time):
            print(self.player.history[slid_time].message)

        out=widgets.interactive_output(fctOut,{"slid_time" :self.player.slider_time})
        
        self.affichage=ipywidgets.HBox([fast_backward,backward,step_backward,pause,step_forward,play,fast_forward,self.player.slider_time,slider])
        VBox.__init__(self,[self.player.view,self.affichage,out])
        

#Class View:
# argument : Labyrinthe
# -> Créer une gridbox contenant les images de notre labyrinthe
 
class View (GridBox):
    #constructeur
    def __init__(self,value):

        self.taille_ligne= len(value.board.plateau[0])
        self.value=value 
        self.items=[]
        GridBox.__init__(self)
        self.layout=ipywidgets.Layout(grid_template_columns="repeat("+str(self.taille_ligne)+", 50px)",grid_column_gap="1px")
        self.create()


            
    #change la value
    def set_value(self,value):
        self.value=value

    #met à jour notre affichage
    def update(self):
        
        laby=self.value
        carte = laby.board.plateau
        for j in range (0,len(carte)):
            
            for i in range (0,len(carte[0])):
                if(j==laby.position.i and i==laby.position.j):
                    tuile= laby.dirToAnt()
                else:
                    tuile = laby.board.get(position(j,i))
                
                
                self.items[j*self.taille_ligne+i].value=deepcopy(Tiles.tile2Png[tuile].value)
                
                
    #renvoie une nouvelle image a partir d'une tuile donnée 
    def toImg(self,tuile):
        pof = tuile.name
        image = "include/laby/tiles_png/" + pof + ".png"
        file = open (image,'rb')
        image_lu = file.read()
        img=(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="flex",
        margin="1" ,padding="0", width="50%"
        )))
        return img

    
    def create(self):
        laby=self.value
        carte = laby.board.plateau
        
        for j in range (0,len(carte)):
            
            for i in range (0,len(carte[0])):
                if(j==laby.position.i and i==laby.position.j):
                    tuile= laby.dirToAnt()
                else:
                    tuile = laby.board.get(position(j,i))
                
                self.items.append(self.toImg(tuile))
                
        self.children=self.items

#fonction qui renvoie un widget en donnant la visualisation 
def ValuePlayerWidget(visualisation):
    player=Player(visualisation)
    app=PlayerView(player) 
  
    return app