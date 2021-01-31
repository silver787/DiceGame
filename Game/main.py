from Game.game_constants import *
from Game.game_classes import *
from Game.game_frames import *
import itertools
import pygame
import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageTk, Image


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.configure(bg=BLUE[0])
        self.resizable(height=False, width=False)
        self.title("Login")
        self.geometry(
            f"{int(WINDOW_WIDTH)}x{int(WINDOW_HEIGHT)}+{int(self.winfo_screenwidth() / 2) - int(WINDOW_WIDTH / 2)}"
            f"+{int(self.winfo_screenheight() / 2) - int(WINDOW_HEIGHT / 2)}")

        for i in itertools.product(range(4), range(6)):
            ALL_DICE[i[0]][i[1]] = Image.open(ALL_DICE[i[0]][i[1]])
            ALL_DICE[i[0]][i[1]] = ALL_DICE[i[0]][i[1]].resize((125, 125), Image.ANTIALIAS)
            ALL_DICE[i[0]][i[1]] = ImageTk.PhotoImage(ALL_DICE[i[0]][i[1]])

        self.colour = BLUE
        self.font_colour = "white"
        self.dice = BLUE_DICE
        self.frame = None
        self.switch_frame(P1Login)

    def switch_frame(self, frame):
        if self.frame:
            self.frame.destroy()

        self.frame = frame(self)
        self.frame.pack()


if __name__ == "__main__":
    root = App()
    root.mainloop()
