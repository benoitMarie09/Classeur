from os import walk, sep
from C_Filters.Filters_frames import Filters
from E_Courses.Cours import Course
from B_Constant.CONSTANT import LEVEL


class Courses_set(list):
    """
    A class that create a list of Cours(class)
    """

    def __init__(self, parent, path: str = None):
        super().__init__()
        self.parent = parent

        # reference list of all parameter in the Courses_set
        self.level1 = []
        self.level3 = []
        self.level2 = []
        self.keys = []
        self.types = []

        # fill up references lists
        if path:
            self.path = path
            self.walk = walk(path, topdown=True)
            for (root, dirs, files) in self.walk:
                for file in files:
                    self.append(Course(self, root+sep+file))
                    self.update_references()

    @property
    def mastr(self):
        if self.parent:
            return self.parent.mastr

    @property
    def all_references(self) -> dict:
        # return ref lists in a dict
        return {
            "Nom": None,
            LEVEL["#1"]: self.level1,
            LEVEL["#2"]: self.level2,
            LEVEL["#3"]: self.level3,
            "Mots clés": self.keys,
            "Type": self.types,
        }

    def filter(self, filters: Filters):
        # Return a new Courses_set that pass the filters
        # And update filters list
        new_set = Courses_set(parent=self.parent)
        filters.reset_references()
        for cours in self:
            if filters.is_OK(cours):
                new_set.append(cours)
        filters.verif_visibility()
        filters.reset_place()
        return new_set

    def update_references(self):
        # Update ref lists
        if not(self[-1][LEVEL["#3"]] in self.level3):
            self.level3.append(self[-1][LEVEL["#3"]])

        if not(self[-1][LEVEL["#2"]] in self.level2):
            self.level2.append(self[-1][LEVEL["#2"]])

        for item in self[-1]["Mots clés"]:
            if not item in self.keys:
                self.keys.append(item)

        if not(self[-1]["Type"] in self.types):
            self.types.append(self[-1]["Type"])

        if not(self[-1][LEVEL["#1"]] in self.level1):
            self.level1.append(self[-1][LEVEL["#1"]])
