import classes.acceuil as acceuil
import tkinter as tk


class MainWindow(object):

    """Création de la fenêtre principale"""

    def __init__(self):
        self.parent = tk.Tk()
        self.fullScreenState = False
        self.parent.bind('<f>', self.togglefullscreen)
        self.parent.title('Mermory')
        self.parent.configure(background='dark blue')
        self.parent.geometry('1280x720+0+0')  # (width x height + posx + posy)
        self.acc = acceuil.Acceuil(self.parent)
        self.acc.acceuil()
        self.parent.mainloop()

    def togglefullscreen(self, event):

        """Active ou désactive le fullscreen"""

        self.fullScreenState = not self.fullScreenState
        self.parent.attributes('-fullscreen', self.fullScreenState)
