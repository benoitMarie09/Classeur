from os import sep
from B_Constant.CONSTANT import LEVEL


class Course(dict):
    """
    A class that collect all the parameters of a fill from it's path in a dict
    """

    def __init__(self, parent, _path: str):
        super().__init__()
        self.parent = parent
        self.path = _path
        self.dir_list = self.path.split(sep)
        self.fill_parameters()

    @property
    def mastr(self):
        return self.parent.mastr

    @property
    def is_on(self) -> bool:
        # Define if Course pass the filter or not
        return self.mastr.filters.is_OK(self)

    def fill_parameters(self) -> None:
        # Fill Course dict with all the parameters from it's path
        self["path"] = self.path

        if len(self.dir_list) > 2:
            self[LEVEL["#1"]] = self.dir_list[1]
        else:
            self[LEVEL["#1"]] = ""

        if len(self.dir_list) > 3:
            self[LEVEL["#2"]] = self.dir_list[2].split("_")[0]
        else:
            self[LEVEL["#2"]] = ""

        if len(self.dir_list) > 4:
            chaplist = self.dir_list[3].split("_")[2:]
            if len(chaplist) == 1:
                self[LEVEL["#3"]] = chaplist[0]
            else:
                texte = chaplist[0]
                for item in chaplist[1:]:
                    texte += " " + item
                self[LEVEL["#3"]] = texte
        else:
            self[LEVEL["#3"]] = ""

        if self.dir_list[-1][0] == "[":
            self["Mots clés"] = self.dir_list[-1].split("]")[
                0].split("[")[-1].split(",")
        else:
            self["Mots clés"] = []

        self["Nom"] = self.dir_list[-1].split("]")[-1].split(".")[
            0].replace("_", " ")

        self["Type"] = self.dir_list[-1].split(".")[-1]
