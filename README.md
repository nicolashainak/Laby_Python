# Laby_Python
Projet Laby en Python Master 1 réaliser par Hainak Nicolas et Cornic Erwan


Objectif : Réimplémenter le jeu Laby ayant était implémenté sous jupyter en C++ en Pyhton.

Notre objectif et de transférer le jeu Laby que nous avons en c++ en Python afin de l'utiliser sous jupyter.
Pour ce faire nous avons "traduit" le jeu de C++ à Python puis nous avons créé un value player Widget afin de l'afficher 
et de pouvoir utiliser un historique. 


[Lien vers la page du cours](https://gitlab.u-psud.fr/nicolas.thiery/ter-jupyter)


# Notre Projet

[Lien vers notre rapport](rapport.ipynb)

[Lien vers notre diaporama](presentation.ipynb)

[Lien vers laby](Laby_final.ipynb)

Notre Binder : [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/nicolashainak/Laby_Python/master)


## Pour l'installation du projet:

Les bibliothéques suivantes doivent être installées:
- notebook
- xeus-cling
- xwidgets
- pip
- matplotlib
- ipywidgets
- rise
- traits

Notre diaporama s'ouvre avec l'extension RISE de Jupyter : le raccourci Alt + r.

Le rapport est un jupyter-notebook classique.

Pour notre labyrinthe:
Vous devez ouvrir le jupyter-notebook nommé Laby_final.ipynb.
La première cellule contient des liens vers les niveaux et les instructions.
Votre but est de faire sortir la fourmi du labyrinthe.
Pour cela une liste de commandes vous est donné en instruction, utilisées les judicieusement afin de trouver le meilleur chemin vers la sortie.
Pour changer de niveau : changer le nom du niveau chargé dans la cellules 2 par l'un de ceux présent dans la liste des niveaux.
