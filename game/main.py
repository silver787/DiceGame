from game.game_frames import *
import itertools
from PIL import ImageTk, Image


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.configure(bg=BLUE[0])
        self.resizable(height=False, width=False)
        self.geometry(
            f"{int(WINDOW_WIDTH)}x{int(WINDOW_HEIGHT)}+{int(self.winfo_screenwidth() / 2) - int(WINDOW_WIDTH / 2)}"
            f"+{int(self.winfo_screenheight() / 2) - int(WINDOW_HEIGHT / 2)}")

        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

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
