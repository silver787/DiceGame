from Game.game_constants import *
import tkinter as tk


class Player:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.roll_1 = 0
        self.roll_2 = 0
        self.calc = ''
        self.roll_again = False

    def reset(self):
        self.roll_1 = 0
        self.rol_2 = 0
        self.calc = ''
        self.roll_again = False


class Game:
    def __init__(self):
        self.round = 0
        self.turn = None


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


class QuitButton(tk.Button):
    def __init__(self, parent, meta_parent, command, last_frame):
        tk.Button.__init__(self, parent, text='Quit', fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[0],
                           command=command)

        self.pack(anchor='nw', pady=5)


class SaveButton(tk.Button):
    def __init__(self, parent, meta_parent, command, last_frame):
        tk.Button.__init__(self, parent, text='Save', fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[0],
                           command=command)

        self.pack(anchor='nw')


class GameTitle(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[0], fg=meta_parent.font_colour,
                          font=(FONT, 30))
        self.grid(column=0, row=0, columnspan=3, pady=4)


class P1Title(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[0],
                          fg=meta_parent.font_colour,
                          width=10)
        self.grid(column=0, row=1, sticky="N")


class Score(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text,
                          bg=meta_parent.colour[0], fg=meta_parent.font_colour, width=10)
        self.grid(column=1, row=1, sticky="N")


class P2Title(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[0],
                          fg=meta_parent.font_colour,
                          width=10)
        self.grid(column=2, row=1, sticky="N")


class P1Frame(tk.Frame):
    def __init__(self, parent, meta_parent):
        tk.Frame.__init__(self, parent, bg=meta_parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                          height=WINDOW_HEIGHT / 4 * 3)
        self.grid(column=0, row=2, sticky="N", padx=5)

        self.pack_propagate(0)


class BorderFrame(tk.Frame):
    def __init__(self, parent, meta_parent):
        tk.Frame.__init__(self, parent, bg=meta_parent.colour[0], width=WINDOW_WIDTH / 100 * 2)
        self.grid(column=1, row=2)


class P2Frame(tk.Frame):
    def __init__(self, parent, meta_parent):
        tk.Frame.__init__(self, parent, bg=meta_parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                          height=WINDOW_HEIGHT / 4 * 3)
        self.grid(column=2, row=2, sticky="N", padx=5)
        self.pack_propagate(0)


class P1Dice1(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P1Dice2(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                         image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P1CalcBox(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          width=50, height=5)

        self.pack(pady=5)


class P2Dice1(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P2Dice2(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P2CalcBox(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          width=50, height=5)
        self.pack(pady=5)


class P1RollButton(tk.Button):
    def __init__(self, parent, meta_parent, command):
        tk.Button.__init__(self, parent, text="ROLL!", bg=meta_parent.colour[1],
                           highlightbackground=meta_parent.colour[1],
                           command=command)
        self.pack()


class P1Info(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, text="OR Press Left Shift!", bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          height=5)

        self.pack()


class P2RollButton(tk.Button):
    def __init__(self, parent, meta_parent, command):
        tk.Button.__init__(self, parent, text="ROLL!", bg=meta_parent.colour[1],
                           highlightbackground=meta_parent.colour[1],
                           command=command)
        self.pack()


class P2Info(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, text="OR Press Return!", bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          height=5)

        self.pack()
