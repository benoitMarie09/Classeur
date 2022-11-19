
from tkinter.messagebox import NO
from tkinter.ttk import Treeview
from tkinter import PhotoImage
from typing import OrderedDict
from E_Courses.courses_set import Courses_set
from D_treeview.Right_click_menu import Menu_click
import subprocess
from B_Constant.CONSTANT import LIGNE_COLORS, LEVEL
from os import path
from pathlib import Path
from os import environ
from sys import platform


class Arbre_de_classement(Treeview):
    def __init__(self, absolute_path, parent, **kw):
        super().__init__(parent, style="Custom.Treeview", **kw)

        self.TV_COLUMNS = {
            "#0": ["Nom", False, 400, 0],
            "#1": [LEVEL["#3"], False, 300, 1],
            "#2": [LEVEL["#2"], False, 100, 2],
            "#3": ["Mots clés", False, 250, 3],
            "#4": ["Type", False, 100, 4],
            "#5": [LEVEL["#1"], False, 100, 5],
        }

        # Création fenêtre arborescente :
        self.parent = parent
        self.abs_path = absolute_path
        self.path = path.relpath(absolute_path)
        self.mes_cours = Courses_set(self, self.path)
        self.head_is_on = False
        self.head_is_click = False
        self.current_columns = None
        self.sorted_column = "#0"
        # Mise en place de colonnes
        self["columns"] = ("#1", "#2", "#3", "#4", "#5")
        self.refresh_columns_size()

        self.image_down = PhotoImage(file='./icon/down_arrow.png')
        self.image_up = PhotoImage(file='./icon/up_arrow.png')
        self.image_blank = PhotoImage(file='./icon/blank.png')
        self.tag_configure('odd', background=LIGNE_COLORS["odd"])
        self.tag_configure('even', background=LIGNE_COLORS["even"])

        # Définitions des en-têtes des colonnes
        self.sort_reverse = {
            "#0": False,
            "#1": False,
            "#2": False,
            "#3": False,
            "#4": False,
            "#5": False,
        }
        self.refresh_heading()

        self.menu_c = Menu_click(self)
        self.bind("<Double-1>", self.open_file)
        self.bind("<Button-3>", self.menu_c.do_popup)
        self.bind('<Motion>', self.mouse_move)
        self.bind('<Button-1>', self.mouse_click)
        self.bind('<ButtonRelease-1>', self.mouse_rel)

    @property
    def mastr(self):
        return self.parent.mastr

    @property
    def tree(self):
        return self

    def afficher_list(self, ensemble_cours):
        self.delete(*self.get_children())
        lign = "even"
        for cours in ensemble_cours:
            if cours.is_on:
                vals = (cours[self.TV_COLUMNS["#1"][0]], cours[self.TV_COLUMNS["#2"][0]], cours[self.TV_COLUMNS["#3"][0]],
                        cours[self.TV_COLUMNS["#4"][0]], cours[self.TV_COLUMNS["#5"][0]], cours["path"])
                self.insert("", "end", text=cours[self.TV_COLUMNS["#0"][0]],
                            values=vals, tags=lign)
                if lign == "even":
                    lign = "odd"
                elif lign == "odd":
                    lign = "even"
        self.update_col()

    def open_file(self, event):
        if self.identify_region(event.x, event.y) == "tree":
            path = self.item(self.selection())['values'][5]
            myEnv = dict(environ)

            toDelete = []
            for (k, v) in myEnv.items():
                if k != 'PATH' and 'tmp' in v:
                    toDelete.append(k)

            for k in toDelete:
                myEnv.pop(k, None)

            shell = False
            if platform == "win32":
                opener = "start"
                shell = True
            elif platform == "darwin":
                opener = "open"
            else:  # Assume Linux
                opener = "xdg-open"

            subprocess.call([opener, path], env=myEnv, shell=shell)

        else:
            pass

    def update_col(self):
        if self.sorted_column == "#0":
            l = [(self.item(k, option="text"), k)
                 for k in self.get_children('')]
        else:
            l = [(self.set(k, self.sorted_column), k)
                 for k in self.get_children('')]
        l.sort(reverse=self.sort_reverse[self.sorted_column])

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

    def treeview_sort_column(self, col, reverse):
        self.sorted_column = col
        self.update_col()
        # image
        for _col in self.TV_COLUMNS.keys():
            if _col == col and reverse == True:
                self.heading(_col, image=self.image_up)
            elif _col == col and reverse == False:
                self.heading(_col, image=self.image_down)
            else:
                self.heading(_col, image=self.image_blank)

        # reverse sort next time
        self.sort_reverse[col] = not self.sort_reverse[col]

    def mouse_move(self, event):
        self.head_is_on = self.identify_region(event.x, event.y) == "heading"
        if self.head_is_click:
            if list(self.TV_COLUMNS.keys()).index(self.identify_column(event.x)) > list(self.TV_COLUMNS.keys()).index(self.current_columns) and self.identify_column(event.x) != "#0":
                if self.identify_column(event.x+self.TV_COLUMNS[self.current_columns][2]) != self.current_columns or "#1":
                    self.switch_columns(self.identify_column(event.x))
            if list(self.TV_COLUMNS.keys()).index(self.identify_column(event.x)) < list(self.TV_COLUMNS.keys()).index(self.current_columns) and self.identify_column(event.x) != "#0":
                if self.identify_column(event.x-self.TV_COLUMNS[self.current_columns][2]) != self.current_columns or "#1":
                    self.switch_columns(self.identify_column(event.x))

    def mouse_click(self, event):
        if self.identify_region(event.x, event.y) == "heading":
            self.head_is_click = True
            self.current_columns = self.identify_column(event.x)
            self.config(cursor="fleur")

    def mouse_rel(self, event):
        if self.head_is_click:
            self.head_is_click = False
            self.current_columns = None

    def refresh_heading(self):
        for col, vals in self.TV_COLUMNS.items():
            self.heading(col, text=vals[0].capitalize(), anchor="w",
                         command=lambda _col=col: self.treeview_sort_column(_col, self.sort_reverse[_col]))

    def refresh_columns_size(self):
        for col, val in self.TV_COLUMNS.items():
            if col != "#5":
                self.column(col, width=val[2],
                            stretch=False)
            else:
                self.column(col, width=val[2],
                            stretch=True)

    def switch_columns(self, col):
        param_A = self.TV_COLUMNS[self.current_columns]
        param_B = self.TV_COLUMNS[col]
        self.TV_COLUMNS[self.current_columns] = param_B
        self.TV_COLUMNS[col] = param_A
        self.current_columns = col
        self.refresh_heading()
        self.refresh_columns_size()
        self.afficher_list(self.mes_cours)

    def update(self):
        self.mes_cours = None
        self.mes_cours = Courses_set(self, path=self.path)
        self.afficher_list(self.mes_cours)
