import pygame
# pygame is used for music
import tkinter as tk
# tkinter is used for the GUI
from PIL import ImageTk, Image
# PIL is used for image processing
from data.constants import *
# constants gets constants needed
from frames import *
# frames gets the different pages made


class Root(tk.Tk):
    """A class that creates the base for all widgets, all the other frames(pages) are added ontop of this one, the
    class also carries out certain processses that are needed for all the other pages to work, such as pygame music
    initialization"""

    def __init__(self):
        tk.Tk.__init__(self)

        self.configure(bg=BLUE[0])
        self.resizable(height=False, width=False)
        self.title("Login")
        self.geometry(
            f"{int(WINDOW_WIDTH)}x{int(WINDOW_HEIGHT)}+{int(self.winfo_screenwidth() / 2) - int(WINDOW_WIDTH / 2)}"
            f"+{int(self.winfo_screenheight() / 2) - int(WINDOW_HEIGHT / 2)}")

        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        self.colour = BLUE
        self.font_colour = "white"
        self.colours_dict = {"blue": [BLUE, "white", BLUE_DICE], "green": [GREEN, "white", GREEN_DICE],
                             "black": [BLACK, "white", BLACK_DICE],
                             "white": [WHITE, "#454545", WHITE_DICE]}

        for x in range(4):
            for y in range(6):
                ALL_DICE[x][y] = Image.open(ALL_DICE[x][y])
                ALL_DICE[x][y] = ALL_DICE[x][y].resize((125, 125), Image.ANTIALIAS)
                ALL_DICE[x][y] = ImageTk.PhotoImage(ALL_DICE[x][y])

        self.dice = BLUE_DICE

        self.frame = None
        self.switch_frame(PlayerOneLoginPage)

    def switch_frame(self, frame, *args):
        """A function that allows the page currently being displayed on the base page(Root) to be changed."""
        if self.frame:
            self.frame.destroy()

        self.frame = frame(self, *args)
        self.frame.pack()


Root().mainloop()
