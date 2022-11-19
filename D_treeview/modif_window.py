from tkinter import Button, Toplevel, StringVar, Label, Frame, Entry
from pathlib import Path
from os import rename, path
import subprocess
from time import ctime
from os import environ
from sys import platform


class Top_prop(Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.selection = self.tree.selection()
        self.path = self.tree.item(self.selection[0])[
            'values'][-1]
        self.geometry("600x300")
        self.minsize(width=600, height=300)
        self.maxsize(height=310)
        self.config(bg="#efefef")

        self.nom_box = Nom_modif(self)
        self.nom_box.place(x=0, y=20, relwidth=1, height=30)

        self.keys_box = Mots_cles_modif(self)
        self.keys_box.place(x=0, y=60, relwidth=1, height=30)

        self.path_box = Path_open(self)
        self.path_box.place(x=0, y=100, relwidth=1, height=30)

        info_type = Info(self,  "Type :", "."+self.get_type())
        info_type.place(x=0, y=140, relwidth=1, height=30)

        self.size = str(round(path.getsize(self.path)/1000, 2))
        info_size = Info(self,  "Size :", self.size+" Ko")
        info_size.place(x=0, y=180, relwidth=1, height=30)

        self.mtime = ctime(path.getmtime(self.path))
        info_mtime = Info(self,  "Dernière modification :",
                          self.mtime)
        info_mtime.configure()
        info_mtime.place(x=0, y=220, relwidth=1, height=30)

        self.apply_btn = Button(self,
                                text="Appliquer",
                                bg='#2c2c2c',
                                fg="#EEEEEE",
                                relief="flat",
                                font="Droid 12",
                                activebackground='#0c5849',
                                activeforeground="white",
                                command=self.apply)

        self.apply_btn.place(y=260, relx=0.65)
        self.quit_btn = Button(self,
                               text="Quitter",
                               bg='#2c2c2c',
                               fg="#EEEEEE",
                               relief="flat",
                               font="Droid 12",
                               activebackground='#0c5849',
                               activeforeground="white",
                               command=self.destroy)
        self.quit_btn.place(y=260, relx=0.2)

    @property
    def tree(self):
        return self.parent.tree

    def get_type_rank(self):
        i = 0
        for item in self.tree.TV_COLUMNS.values():
            if item[0] == "Type":
                return i
            i += 1

    def get_type(self):
        rank = self.get_type_rank()-1
        type = self.tree.item(self.selection[0])[
            'values'][rank]
        return type

    def get_motscles_rank(self):
        i = 0
        for item in self.tree.TV_COLUMNS.values():
            if item[0] == "Mots clés":
                return i
            i += 1

    def get_keys_list(self):
        rank = self.get_motscles_rank()-1
        keys = self.tree.item(self.selection[0])[
            'values'][rank].replace(" ", ",")
        return keys

    def apply(self):
        new_mots_cles = "["+self.keys_box.entry_text.get()+"]"
        print(new_mots_cles)
        new_name = self.nom_box.entry_text.get().replace(" ", "_")
        type = self.get_type()
        my_path = Path(self.path).absolute()
        old_file = my_path
        new_file = path.join(my_path.parent, new_mots_cles+new_name+"."+type)

        rename(old_file, new_file)
        self.tree.update()
        self.destroy()


class Info(Frame):
    def __init__(self, parent, texte, info, width_text=160, x_info=200, relwidth_info=0.5):
        super().__init__(parent)
        self.parent = parent
        self.selection = self.tree.selection()
        self.label = Label(self, text=texte, anchor="w", bg="#efefef", fg="#28050c",
                           font="Droid 11 bold")
        self.info = Label(self, text=info, anchor="w", bg="#efefef", fg="#28050c",
                          font="Droid 11 ")
        self.label.place(x=20, width=width_text)
        self.info.place(x=x_info, y=0, relwidth=relwidth_info)
        self.config(bg="#efefef")

    @property
    def tree(self):
        return self.parent.tree


class Modif_entry(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selection = self.tree.selection()
        self.orig_text = ""
        self.entry_text = StringVar()
        self.entry_text.set(self.orig_text)
        self.config(bg="#efefef")
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.label = Label(self, anchor="w", bg="#efefef", fg="#28050c",
                           font="Droid 11 bold")
        self.label.place(x=20, width=160)

        self.entry = Entry(self,
                           textvariable=self.entry_text,
                           state="readonly",
                           bd=0,
                           bg="#efefef",
                           fg="#28050c",
                           highlightbackground="#126385",
                           relief="flat",
                           highlightthickness=3,
                           highlightcolor="#126385",
                           selectbackground="#18b293",
                           selectforeground='#28050c',
                           selectborderwidth=0,
                           readonlybackground="#dfdfdf")

        self.entry.place(x=200, y=0, relwidth=0.5)
        self.entry.bind("<Configure>", self.on_resize)

        self.modif_btn = Button(self,
                                text="Modifier",
                                bg='#2c2c2c',
                                fg="#EEEEEE",
                                relief="flat",
                                font="Droid 11",
                                activebackground='#0c5849',
                                activeforeground="white",
                                command=self.modif)

        self.modif_btn.place(x=205, y=-5, relx=0.5)

    @property
    def tree(self):
        return self.parent.tree

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        # self.entry.configure(width=int(self.width/2))

    def modif(self):
        self.entry.configure(state="normal")
        self.modif_btn.configure(text="annuler", command=self.cancel)

    def cancel(self):
        self.entry_text.set(self.orig_text)
        self.entry.configure(state="readonly")
        self.modif_btn.configure(text="Modifier", command=self.modif)


class Nom_modif(Modif_entry):
    def __init__(self, parent):
        super().__init__(parent)
        self.orig_text = self.get_text()
        self.entry_text.set(self.orig_text)
        self.label.configure(text="Nom :")

    def get_nom_rank(self):
        i = 0
        for item in self.tree.TV_COLUMNS.values():
            if item[0] == "Nom":
                return i
            i += 1

    def get_text(self):
        return self.tree.item(self.selection[0])["text"]


class Mots_cles_modif(Modif_entry):
    def __init__(self, parent):
        super().__init__(parent)
        self.orig_text = self.get_keys_list()
        self.entry_text.set(self.orig_text)
        self.label.configure(text="Mot clés :")

    def get_motscles_rank(self):
        i = 0
        for item in self.tree.TV_COLUMNS.values():
            if item[0] == "Mots clés":
                return i
            i += 1

    def get_keys_list(self):
        rank = self.get_motscles_rank()-1
        keys = self.tree.item(self.selection[0])[
            'values'][rank].replace(" ", ",")
        return keys


class Path_open(Modif_entry):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.path = Path(parent.path).absolute()
        self.orig_text = path.dirname(self.path)
        self.entry_text.set(self.orig_text)
        self.label.configure(text="Dossier parent :")
        self.modif_btn.configure(text="Ouvrir", command=self.open)

    def open(self):
        path = self.orig_text
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
        else: # Assume Linux
            opener = "xdg-open"

        subprocess.call([opener, path], env=myEnv, shell=shell)
