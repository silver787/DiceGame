from Game.game_constants import *
import tkinter as tk


class Player:
    def __init__(self, username):
        self.username = username
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


class AlertLabel(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Label.__init__(self, parent, text=text, fg='orange',
                          bg=meta_parent.colour[1])
        self.pack(padx=padx, pady=pady)


class UnderlineSubtitle(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Label.__init__(self, parent, text=text, fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1], font=(FONT, 25, "underline"))
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
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1],
                           command=command)

        self.pack(padx=padx, pady=pady)


class MenuButton(tk.Button):
    def __init__(self, parent, meta_parent, text, command, x, y, padx, pady):
        tk.Button.__init__(self, parent, text=text, fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1],
                           width=x, height=y,
                           command=command)

        self.pack(padx=padx, pady=pady)


class BackButton(tk.Button):
    def __init__(self, parent, meta_parent, last_frame):
        tk.Button.__init__(self, parent, text='Back', fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1],
                           command=lambda: meta_parent.switch_frame(last_frame))

        self.pack(anchor='nw', padx=5, pady=5)


class VolumeScale(tk.Scale):
    def __init__(self, parent, meta_parent, command, padx, pady):
        tk.Scale.__init__(self, parent, orient="horizontal",
                          bg=meta_parent.colour[1], fg=meta_parent.font_colour,
                          length=80, troughcolor=meta_parent.colour[1], showvalue=0,
                          highlightcolor=meta_parent.colour[1],
                          highlightbackground=meta_parent.colour[1],
                          activebackground=meta_parent.colour[1], command=command)
        self.pack(padx=padx, pady=pady)


class ThemeCheckbox(tk.Checkbutton):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Checkbutton.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                                fg=meta_parent.font_colour, command=lambda: parent.change_theme(text.lower(), self))
        self.deselect()
        self.pack(padx=padx, pady=pady)
