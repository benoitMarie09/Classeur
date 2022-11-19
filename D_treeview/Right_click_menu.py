from tkinter import Menu
import subprocess
from shutil import copy
from os import mkdir, path
from time import strftime
from D_treeview.modif_window import Top_prop


class Menu_click(Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=0)
        self.parent = parent
        self.config(background="#126385", foreground="#EEEEEE",
                    activebackground="#18b293", activeforeground="#28050c")
        self.add_command(label="Ouvrir", command=lambda: self.open(self))
        self.add_command(label="Modifier",
                         command=lambda: self.rm_mots_cles(self))
        self.add_command(label="À imprimer",
                         command=lambda: self.copy_to_print(self))
        parent.bind("<Button-3>", lambda: self.do_popup(self))

    def do_popup(self, event):
        iid = self.parent.identify_row(event.y)
        if iid in self.parent.selection():
            print(len(self.parent.selection()))
            if len(self.parent.selection()) > 1:
                self.disable_multiple_item_command()
            else:
                self.enable_multiple_item_command()
            self.tk_popup(event.x_root, event.y_root)
        elif iid:
            # mouse pointer over item
            self.parent.selection_set(iid)
            print(len(self.parent.selection()))
            if len(self.parent.selection()) > 1:
                self.disable_multiple_item_command()
            else:
                self.enable_multiple_item_command()
            self.tk_popup(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    @property
    def mastr(self):
        return self.parent.mastr

    @property
    def tree(self):
        return self.parent.tree

    def open(self, event):

        _paths = [self.parent.item(iid)['values'][5]
                  for iid in self.parent.selection()]

        for _path in _paths:
            subprocess.call(('xdg-open', _path))

    def copy_to_print(self, event):

        _paths = [self.parent.item(iid)['values'][5]
                  for iid in self.parent.selection()]

        if not path.exists("./À imprimer"):
            mkdir("./À imprimer")

        today = strftime('%d'+"_"+'%m'+"_"+'%Y')
        destination = "./À imprimer/"+today
        if not path.exists(destination):
            mkdir(destination)
        for _path in _paths:
            copy(_path, destination)

    def rm_mots_cles(self, event):
        Top_prop(self.tree)

    def enable_multiple_item_command(self):
        self.entryconfigure("Ouvrir", state="normal")
        self.entryconfigure("Modifier", state="normal")

    def disable_multiple_item_command(self):
        self.entryconfigure("Ouvrir", state="disable")
        self.entryconfigure("Modifier", state="disable")
