from tkinter.ttk import Frame, Label, Checkbutton
from E_Courses.Cours import Course
from B_Constant.CONSTANT import SCROLL_STEP, ANIM_DELAY, LEVEL, H_CHBOX, H_LABEL, ANIM_STEP
from tkinter import PhotoImage, StringVar, IntVar, Entry


class Filters(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.offset = 0
        self.frames = []
        self.references = self.parent.mes_cours.all_references
        i = 0
        for name, val in self.references.items():
            self.frames.append(Checkbox_filtre(
                self, name, i, val) if val else Entry_filtre(self, name, i))
            i += 1
        self.reset_place(True)

    def reset_references(self):
        self.references = {
            "Nom": None,
            LEVEL["#1"]: [],
            LEVEL["#2"]: [],
            LEVEL["#3"]: [],
            "Mots clés": [],
            "Type": [],
        }

    @property
    def mastr(self):
        return self.parent.mastr

    @property
    def hauteur(self):
        result = 0
        for frm in self.frames:
            result += frm.hauteur
        return result

    def is_OK(self, crs: Course) -> bool:
        result = True
        for frm in self.frames:
            # REMPLISSAGE DES REFERENCES
            if frm.name != "Nom":
                if frm.name == "Mots clés":
                    for item in crs[frm.name]:
                        if not item in self.references[frm.name]:
                            self.references[frm.name].append(item)
                elif not(crs[frm.name] in self.references[frm.name]):
                    self.references[frm.name].append(crs[frm.name])
            # VALIDATION DU COURS
            result = result and frm.is_OK(crs)
            if not result:
                break

        return result

    def verif_visibility(self):
        for frm in self.frames:
            if type(frm) == type(Checkbox_filtre()):
                frm.verif_visibility()

    def reset(self):
        self.parent.classeur.afficher_list(
            self.parent.mes_cours.filter(self))

    def reset_place(self, init=False):
        if self.hauteur <= self.parent.win_height:
            self.offset = 0
        elif self.offset < self.parent.win_height - self.hauteur:
            self.offset = self.parent.win_height - self.hauteur

        h = int(self.offset)
        transition = False
        for i in range(len(self.frames)):
            self.frames[i].place(x=0, y=h, relwidth=1,
                                 height=self.frames[i].hauteur)
            if self.frames[i].fold_transition:
                self.frames[i].update_hauteur()
                transition = True
            h += self.frames[i].hauteur

        if not init:
            self.parent.reset_place()
        if transition:
            self.after(ANIM_DELAY, self.reset_place)

    def scroll(self, event=None):
        mouv = "UP"
        if event.num:
            if event.num == 4:
                mouv = "Down"
        if event.delta:
            if int(event.delta) < 0:
                mouv = "Down"

        if self.hauteur > self.parent.win_height:
            min_offset = self.parent.win_height - self.hauteur
            if mouv == "UP":
                self.offset -= SCROLL_STEP
                if self.offset < min_offset:
                    self.offset = min_offset
            else:
                self.offset += SCROLL_STEP
                if self.offset > 0:
                    self.offset = 0
        self.reset_place()


class Box_filtre(Frame):
    def __init__(self, parent, name, order):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.fold = True
        self.hauteur = 0
        self.order = order
        self.image_down = PhotoImage(file="./icon/down_chevron.png")
        self.image_right = PhotoImage(file="./icon/right_chevron.png")
        self.label = Label(self,
                           text=self.name.replace("_", " ")+" :",
                           image=self.image_right,
                           compound='left', style="Custom.TLabel")
        self.refresh_label()
        self.label.place(x=0, y=0, height=H_LABEL,
                         relwidth=1)
        self.label.bind("<ButtonRelease-1>", self.toggle_fold)
        self.label.bind("<MouseWheel>", self.parent.scroll)
        self.label.bind("<Button-4>", self.parent.scroll)
        self.label.bind("<Button-5>", self.parent.scroll)

    @ property
    def mastr(self):
        return self.parent.mastr

    def toggle_fold(self, event):
        self.fold = not self.fold
        self.parent.reset_place()
        self.refresh_label()

    @ property
    def hauteur_cible(self):
        return H_LABEL + H_CHBOX * (not self.fold) + 2 * self.fold

    @ property
    def fold_transition(self) -> bool:
        return self.hauteur != self.hauteur_cible

    def update_hauteur(self):
        if self.hauteur < self.hauteur_cible:
            self.hauteur += ANIM_STEP
            if self.hauteur > self.hauteur_cible:
                self.hauteur = self.hauteur_cible
        elif self.hauteur > self.hauteur_cible:
            self.hauteur -= ANIM_STEP
            if self.hauteur < self.hauteur_cible:
                self.hauteur = self.hauteur_cible

    def is_OK(self, ref: Course) -> bool:
        return True

    def refresh_label(self):
        if not self.fold:
            self.label.configure(image=self.image_down)
            self.label.image = self.image_down
        if self.fold:
            self.label.configure(image=self.image_right)
            self.label.image = self.image_right


class Entry_filtre(Box_filtre):
    def __init__(self, parent, name, order):
        super().__init__(parent, name, order)

        self.var = StringVar()
        self.entry = Entry(self, textvariable=self.var)
        self.var.trace_add('write', self.rachaichir)
        self.entry.place(x=0, y=H_LABEL, height=H_CHBOX, relwidth=1)
        self.entry.bind("<MouseWheel>", self.parent.scroll)

    @property
    def mastr(self):
        return self.parent.mastr

    def rachaichir(self, *args):
        self.parent.reset()

    def is_OK(self, ref: Course) -> bool:
        return self.var.get() == "" or self.var.get() in ref[self.name]


class Checkbox_filtre(Box_filtre):
    def __init__(self, parent=None, name=None, order=None, val_list=None):
        if parent:
            super().__init__(parent, name, order)
            val_list.sort()
            self.val_list = val_list
            self.visi_list = val_list
            self.var_Type = {ref: IntVar() for ref in self.val_list}
            self.chBs_Type = [Checkbutton(self, text=ref, variable=self.var_Type[ref], style="Custom.TCheckbutton",
                                          command=self.parent.reset) for ref in self.val_list]
            for i in range(len(self.chBs_Type)):
                self.chBs_Type[i].place(
                    x=0, y=H_LABEL + H_CHBOX * i, height=H_CHBOX, relwidth=1)
                self.chBs_Type[i].bind("<MouseWheel>", self.parent.scroll)
                self.chBs_Type[i].bind("<Button-4>", self.parent.scroll)
                self.chBs_Type[i].bind("<Button-5>", self.parent.scroll)

    @property
    def mastr(self):
        return self.parent.mastr

    def verif_visibility(self):
        self.visi_list = self.parent.references[self.name]
        i = 0
        for cb in self.chBs_Type:
            if cb.cget("text") in self.visi_list:
                cb.place(x=0, y=H_LABEL + H_CHBOX * i,
                         height=H_CHBOX, relwidth=1)
                i += 1
            else:
                cb.place_forget()

    @property
    def hauteur_cible(self):
        return H_LABEL + H_CHBOX * len(self.visi_list) * (not self.fold) + 2 * self.fold

    @property
    def values(self):
        test = True
        result = []
        for ref, val in self.var_Type.items():
            if val.get():
                result.append(ref)
                test = False
        if test:
            return self.val_list
        else:
            return result

    def is_OK(self, ref: Course) -> bool:
        if self.name == "Mots clés":
            for item in ref[self.name]:
                if item in self.values:
                    return True
            return False
        else:
            return ref[self.name] in self.values
