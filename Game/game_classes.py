from Game.game_constants import *
import tkinter as tk


class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0



class TitleLabel(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):

        tk.Label.__init__(self, parent, text=text, font=(FONT, TITLE_FONT_SIZE),
                          fg=meta_parent.font_colour, bg=meta_parent.colour[1])
        self.pack(padx=padx, pady=pady)


class TextLabel(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):

        tk.Label.__init__(self, parent, text=text, fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1])
        self.pack(padx=padx, pady=pady)


class WatermarkLabel(tk.Label):
    def __init__(self, parent, meta_parent):

        tk.Label.__init__(self, parent, text="© Toby Hogan 2020", fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1], font=(None, 10))
        self.pack(side="bottom")



class TextEntry(tk.Entry):
    def __init__(self, parent, meta_parent, show, padx, pady):

        tk.Entry.__init__(self, parent, fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1], borderwidth=1, relief='flat', show=show)
        self.pack(padx=padx, pady=pady)


class TextButton(tk.Button):
    def __init__(self, parent, meta_parent, text, command, padx, pady):
        tk.Button.__init__(self, parent, text=text, fg='black',
                          bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1], command=command)

        self.pack(padx=padx, pady=pady)



