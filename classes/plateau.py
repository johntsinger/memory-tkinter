import os
import random
import tkinter as tk
import classes.acceuil as acceuil
from PIL import Image
from module.decorator import *


class Plateau(tk.Frame):

    """Création du plateau"""

    def __init__(self, parent, state, nombre_carte, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.state = state
        self.nombre_carte = nombre_carte
        self.liste_canvas = []  # liste des canvas (cartes)
        self.liste_cartes = []  # liste des cartes : tuple (id du canvas, image)
        self.liste_images = []  # liste des image tk.PhotoImage
        self.liste_bind = []  # liste des bind
        self.carte_choisi = []  # liste des 2 carte choisie
        self.liste_widgets = []  # liste des widgets
        self.liste_gif = []  # liste des images du gif
        self.trouver = 0  # compteur des cartes trouvées
        self.canvas = None  # canvas principal
        self.image = None  # PhotoImage pour les images des cartes et du gif
        self.label = None  # label pour le gif

    def plateau(self):

        """Création du plateau"""

        # configuration de la fenêtre
        # self.fullScreenState = True
        # self.parent.attributes('-fullscreen', self.fullScreenState)
        self.parent.configure(background='white')

        # création du canvas contenant les canvas qui serviront de carte
        self.canvas = tk.Canvas(self.parent, bg='ivory')
        self.canvas.grid(row=0, column=0, sticky='nw')
        self.liste_widgets.append(self.canvas)

        # création du bouton acceuil
        bou = tk.Button(self.parent, text='Acceuil', height=3, width=15, font=10,
                        command=self.acceuil)
        bou.grid(row=1, column=0)
        self.liste_widgets.append(bou)

        self.resize()
        column, line = self.create_carte(0, 0)
        self.canvas.configure(width=(column * (100 + 20)) + 20,
                              height=line * (100 + 20) + 20)
        self.canvas.update()  # nessécaire pour appliquer la taille
        self.canvas.grid_propagate(0)
        self.binds()

    def acceuil(self):

        """Action du boutton acceuil"""

        self.clear()
        acc = acceuil.Acceuil(self.parent)
        acc.acceuil()

    def clear(self):

        """Supprime tous les widgets"""

        if self.liste_widgets:
            for elt in self.liste_widgets:
                elt.destroy()
            self.liste_widgets.clear()
            self.parent.configure(background='dark blue')

    def resize(self):

        """Redimentionne les images du dossier si la taille de l'image n'est
        pas (100, 100) et enregistre l'image redimentionnée'"""

        path = "images/{}".format(self.state)
        for elt in os.listdir(path):
            file = os.path.join(path, elt)
            image = Image.open(file)
            if image.size != (100, 100):
                image = image.resize((100, 100), Image.ANTIALIAS)
                image.save(file, 'png')

    def create_liste_images(self):

        """Créé la liste des images en fonction du nombre de carte choisie"""

        path = "images/{}".format(self.state)
        for elt in os.listdir(path):
            file = os.path.join(path, elt)
            self.image = tk.PhotoImage(file=file)
            self.liste_images.append(self.image)
            random.shuffle(self.liste_images)
        self.liste_images = self.liste_images[0:(self.nombre_carte // 2)]
        self.liste_images = self.liste_images * 2
        random.shuffle(self.liste_images)

    @mini("nombre_carte")
    def create_carte(self, column, line):

        """
        Créé les canvas (cartes) en fonction du nombre de cartes
        Méthode décorée pour calculer le meilleur alignement
        :param column: int, le nombre de carte par colone
        :param line: int, le nombre de carte par ligne
        :return column, line: le nombre de colones et de lignes
        """

        # Création de la liste des images
        self.create_liste_images()

        # Création des canvas (cartes)
        x, y = 0, 0
        for i in range(self.nombre_carte):
            if i % line == 0:
                y += 1
                x = 0

            can = tk.Canvas(self.canvas, bg='grey', width=100, height=100,
                            highlightbackground='black')
            self.canvas.create_window(0, 0, window=can)
            can.grid(row=0 + y, column=0 + x, padx=10, pady=10)
            self.liste_canvas.append(can)
            x += 1

        for elt in self.liste_canvas:
            self.liste_cartes.append((elt, self.liste_images.pop(0)))

        return column, line

    def binds(self):

        """Bind chaque canvas (cartes) sur le clique de la souris"""

        for elt in self.liste_canvas:
            bind = elt.bind('<Button-1>', self.click)
            self.liste_bind.append(bind)

    def unbinds(self):

        """Supprime le bind de chaque canvas du clique de la souris"""

        for elt in self.liste_canvas:
            elt.unbind('<Button-1>')

    def click(self, event):

        """Gestionnaire d'évènement du clique de la souris.
        Affiche l'image dans le canvas correspondant
        :param event:
        """

        # nom de du canvas ou le clique a été enregistré
        num = event.widget
        for elt in self.liste_cartes:
            if num == elt[0]:
                elt[0].create_image(0, 0, image=elt[1], anchor='nw')
                elt[0].configure(highlightbackground='blue')
                if elt not in self.carte_choisi:
                    self.carte_choisi.append(elt)

        if len(self.carte_choisi) == 2:
            self.unbinds()
            self.modify_border()
            self.canvas.after(500, self.verify)

    def verify(self):

        """Verifie si les deux cartes choisi sont identiques
        Si elles sont identiques supprime les canvas des deux cartes
        Sinon enlève l'image du canvas
        """

        if self.carte_choisi[0][1] != self.carte_choisi[1][1]:
            for elt in self.carte_choisi:
                elt[0].delete('all')
                elt[0].configure(highlightbackground='black')
        else:
            for elt in self.carte_choisi:
                elt[0].delete('all')
                elt[0].configure(bg='ivory', highlightthickness=0)
                self.liste_canvas.remove(elt[0])
            self.trouver += 2

        self.carte_choisi = []
        self.binds()

        if self.trouver == self.nombre_carte:
            self.canvas.destroy()
            self.label = tk.Label(self.parent, bg='black', text='YOU WIN', font=("Courier", 110),
                                  fg='red', compound='center')
            self.label.grid(row=0, column=0, sticky='nw')
            self.liste_widgets.append(self.label)
            self.gif()
            self.animated(0, 0)

    def gif(self):

        """Crée une image Photoimage avec chaque image du gif
        et l'ajoute a une liste"""

        name = [image for image in os.listdir('images/fireworks')]
        name.sort()
        for image in name:
            self.image = tk.PhotoImage(file='images/fireworks/' + image)
            self.liste_gif.append(self.image)

    def animated(self, ind, i):

        """Anime le gif : charge chaque image et l'affiche avec un délai de
        50ms et affiche un texte par dessus"""

        # Couleur du text
        liste = ['red', 'white', 'green', 'white', 'blue', 'white',
                 'yellow', 'white']
        # Dernier indice
        last = len(self.liste_gif) - 1
        # Si l'index = l'index du dernier elt de la liste recommence a l'index 0
        # Permet la boucle du gif
        if ind == last:
            ind = 0
        # Pour le texte
        if i == len(liste) - 1:
            i = 0
        if ind % 2:
            i += 1

        self.label.configure(image=self.liste_gif[ind], fg=liste[i])
        self.label.after(50, self.animated, ind + 1, i)

    def modify_border(self):

        """Modifie la couleur de la ligne de focus lorsque le canvas
        n'a pas le focus. Si les deux cartes sont identique en vert
        sinon en rouge
        """

        if self.carte_choisi[0][1] != self.carte_choisi[1][1]:
            for elt in self.carte_choisi:
                elt[0].configure(highlightbackground='red')
        else:
            for elt in self.carte_choisi:
                elt[0].configure(highlightbackground='green')
