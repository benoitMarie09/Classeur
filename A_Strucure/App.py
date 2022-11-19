from dataclasses import field
from faulthandler import disable
from tkinter import UNDERLINE, Tk
from tkinter.ttk import Style
from D_treeview.Courses_treeview import Arbre_de_classement
from C_Filters.Filters_frames import Filters
from B_Constant.CONSTANT import CUSTOM_LAYOUTS, LARGEUR_FILTRE, CUSTOM_STYLES, CUSTOM_MAPS, BACKGROUND_COLOR
import os


class Classeur(Tk):
    def __init__(self):
        super().__init__()

        # Ajout d'un titre à la fenêtre principale :
        self.title("Mon classeur")
        self.config(bg=BACKGROUND_COLOR, width=1530, height=1000)
        self.win_height = 1000
        self.win_width = 1600
        self.style = Style()

        self.classeur = Arbre_de_classement(
            os.getcwd()+"/cours", self)

        self.classeur.place(x=LARGEUR_FILTRE, y=0, relwidth=1,
                            width=-LARGEUR_FILTRE, relheight=1)

        self.filters = Filters(self)
        self.filters.place(x=0, y=0, width=LARGEUR_FILTRE,
                           height=self.filters.hauteur)

        self.filters.reset()
        self.classeur.bind("<Configure>", self.on_Resize)

        # Pick a theme
        self.style.theme_use("clam")

        for c_style, dic in CUSTOM_STYLES.items():
            self.style.configure(c_style, **dic)

        for c_map, dic in CUSTOM_MAPS.items():
            self.style.map(c_map, **dic)

        for c_layout, list in CUSTOM_LAYOUTS.items():
            self.style.layout(c_layout, list)

            # Affichage de la fenêtre créée :
        self.mainloop()

    @ property
    def mastr(self):
        return self

    @ property
    def mes_cours(self):
        return self.classeur.mes_cours

    def on_Resize(self, event):
        self.win_height = int(event.y) + int(event.height)
        self.win_width = int(event.x) + int(event.width)

    def reset_place(self):
        self.filters.place_forget()
        self.filters.place(x=0, y=0, width=LARGEUR_FILTRE,
                           height=self.filters.hauteur)
