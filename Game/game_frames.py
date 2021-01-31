from Game.game_classes import *
from Game.game_constants import *
import Game.game_database as database
import tkinter as tk


class P1Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent

        self.title = TitleLabel(self, self.parent, 'Login', 0, 30)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_button = TextButton(self, self.parent, 'Confirm', lambda: self.login(), 0, 20)
        self.create_account_label = TextLabel(self, self.parent, "Don't have an account?\n\nCreate an account:", 0, 30)
        self.create_account_button = TextButton(self, self.parent, 'Confirm',
                                                lambda: self.parent.switch_frame(P1Create), 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)

    def login(self):
        global p1

        username, password = self.username_entry.get(), self.password_entry.get()

        if database.check_user(username, password):
            p1 = Player(username, password)
            database.reveal_users_table()

