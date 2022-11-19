
# Names of directories levels
LEVEL = {
    "#1": "Date",
    "#2": "Niveau",
    "#3": "Chapitre"
}


H_CHBOX = 25
H_LABEL = 32

SCROLL_STEP = 40
ANIM_DELAY = 20
ANIM_STEP = 3000
ICO = {"croissant": "↗", "decroissant": "↘", "monter": "⇑", "descendre": "⇓"}

LARGEUR_FILTRE = 300


CONF_CHBOX = {
    "bg": "lightgrey",
    "bd": 0,
    "padx": 20,
    "font": ("Arial", 10),
    "anchor": "w",
    "relief": "flat",
    "overrelief": "flat",
    "offrelief": "flat",
    "activebackground": "lightgrey"
}
CONF_FILTRES = {
    "bg": "lightgrey",
    "bd": 0
}
CONF_FILTRE = {
    "bg": "lightgrey",
    "bd": 0
}

CONF_TITRE = {
    "font": ("Arial", 15),
    "bg": "#555555",
    "fg": "#DDDDDD",
    "bd": 0,
    "justify": "left"
}


CONF_BUTTON = {
    "bg": "darkgrey",
    "font": ("Arial", 20),
    "activebackground": "darkgrey"
}

LIST_ICONS = """
←	↑	→	↓	↔	↕	↖	↗	↘   ↙   ↚   ↛   ↜   ↝   ↞   ↟   ↠
↡   ↢   ↣   ↤   ↥   ↦   ↧   ↨   ↩   ↪   ↫   ↬   ↭   ↮   ↯   ↰   ↱
↲   ↳   ↴   ↵   ↶   ↷   ↸   ↹   ↺   ↻   ↼   ↽   ↾   ↿   ⇀   ⇁   ⇂
⇃   ⇄   ⇅   ⇆   ⇇   ⇈   ⇉   ⇊   ⇋   ⇌   ⇍   ⇎   ⇏   ⇐   ⇑   ⇒
⇓   ⇔   ⇕   ⇖   ⇗   ⇘   ⇙   ⇚   ⇛   ⇜   ⇝   ⇞   ⇟   ⇠   ⇡   ⇢   ⇣
⇤   ⇥   ⇦   ⇧   ⇨   ⇩   ⇪   ⇫   ⇬   ⇭   ⇮   ⇯   ⇰   ⇱   ⇲   ⇳   ⇴
⇵   ⇶   ⇷   ⇸   ⇹   ⇺   ⇻   ⇼   ⇽   ⇾   ⇿   """


LIGNE_COLORS = {
    "even": "#F7F7F7",
    "odd": "#efefef"
}

BACKGROUND_COLOR = "#2F2F2F"

CUSTOM_STYLES = {

    "Custom.TFrame": {
        "background": "#555555"
    },

    "Custom.TLabel": {  # paramètre des label des checkbuttons
        "foreground": "#EEEEEE",
        "background": "#2c2c2c",
        "font": "Droid 12"
    },

    "Custom.TCheckbutton": {  # paramètre des checkbuttons
        "foreground": "#EEEEEE",
        "background": "#126385",
        "padding": [0, 0, 0, 0],
        "font": "Droid 11"
    },

    "Custom.Treeview": {  # paramètre du treeview
        "background": "#CCCCCC",
        "fieldbackground": "#171616",
        "foreground": "#28050c",
        "highlightthickness": 0,
        "bd": 0,
        "rowheight": 25,
        "font": ("Droid  11")
    },

    "Custom.Treeview.Heading": {  # paramètre de l'en tête du treeview
        "foreground": "#EEEEEE",
        "background": '#2c2c2c',
        "relief": "flat",
        "font": "Droid 13"
    }
}

CUSTOM_MAPS = {

    "Custom.TLabel": {
        "foreground": [('active',  '#222222')],
        "background": [('active', '#0c5849')]},

    "Custom.TCheckbutton": {
        "font": [('selected', "Droid  11 italic bold"), ],
        "background": [("active", "#18b293")],
        "foreground": [('active',  '#28050c')]},

    "Custom.Treeview": {
        "background": [("selected", "#18b293")],
        "foreground": [('selected',  '#28050c')]},

    "Custom.Treeview.Heading": {
        "foreground": [('active',  'white')],
        "background": [('active', '#0c5849')]},
}

CUSTOM_LAYOUTS = {"Custom.Treeview":
                  [('Treeview.treearea', {
                      'sticky': 'nswe'})]

                  }
