import classes.plateau as plateau
import tkinter as tk


class Acceuil(tk.Frame):

    """Création de l'acceuil"""

    VALS = ["animaux", "fruits"]

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.liste_widgets = []  # liste des widgets
        self.photo = None
        self.state = 'animaux'
        self.scale = None
        self.scale_val = {'animaux': 72, 'fruits': 60}  # Enregistre la valeur du scale
        self.varGr = None

    def acceuil(self):

        """Création de l'acceuil"""

        # Canevas contenant l'image
        can = tk.Canvas(self.parent, width=1280, height=300, bg='white')
        self.photo = tk.PhotoImage(file='images/memory.gif')
        can.create_image(640, 150, image=self.photo)
        can.grid(row=0, column=0, columnspan=5, sticky='n')
        self.liste_widgets.append(can)

        # Boutons radio
        self.varGr = tk.StringVar()
        self.varGr.set(self.state)
        for i in range(len(self.VALS)):
            texte = '{} :\n{} cartes'.format(
                        self.VALS[i].capitalize(), self.scale_val[self.VALS[i]])
            radio = tk.Radiobutton(self.parent, variable=self.varGr,
                                   text=texte, value=self.VALS[i],
                                   bg='white', width=15, height=3, font=15,
                                   command=self.get_event_radio)
            radio.grid(row=1 + i, column=2, pady=5)

            self.liste_widgets.append(radio)

        # Scale pour le nombre de cartes
        self.scale = tk.Scale(self.parent, orient='horizontal', from_=32, to=72,
                              resolution=8, tickinterval=8, length=350,
                              label='Nombre de cartes', bg='white',
                              command=self.get_event_scale)
        self.scale.grid(row=3, column=2, pady=5)
        self.scale.set(self.scale_val[self.state])
        self.liste_widgets.append(self.scale)

        # Boutons jouer
        bou = tk.Button(self.parent, text='Jouer', command=self.jouer,
                        width=15, height=3, font=15)
        bou.grid(row=4, column=2, pady=5)
        self.liste_widgets.append(bou)

        # Label
        texte = 'Appuyer sur <F> permet de passer en plein écrant'
        label = tk.Label(self.parent, text=texte, font=15, bg='dark blue', fg='white')
        label.grid(row=5, column=2, pady=30)
        self.liste_widgets.append(label)

    def jouer(self):

        """Action du boutton jouer"""

        nombre_carte = self.scale.get()
        for elt in self.liste_widgets:
            elt.destroy()
        plat = plateau.Plateau(self.parent, self.state, nombre_carte)
        plat.plateau()

    def get_event_radio(self):

        """Modifie self.scale en fonction du bouton radio
        selectionner"""

        self.state = self.varGr.get()
        if self.state == "animaux":
            self.scale.configure(from_=32, to=72, resolution=8,
                                 tickinterval=8)
            self.scale.set(self.scale_val[self.state])

        if self.state == "fruits":
            self.scale.configure(from_=20, to=60, resolution=10,
                                 tickinterval=10)
            self.scale.set(self.scale_val[self.state])

    def get_event_scale(self, val):

        """Modifie les boutons radio en fonction du nombre de carte selectionné
        :param val: int, valeur renvoyée par self.scale
        """

        for elt in self.liste_widgets:
            if elt.winfo_class() == 'Radiobutton':  # Class du widget
                if elt.cget('value') == self.state:  # Compare l'option 'value' à self.state
                    elt.configure(text='{} :\n{} cartes'.format(
                        self.state.capitalize(), val))
                    self.scale_val[self.state] = self.scale.get()
