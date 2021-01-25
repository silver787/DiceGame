import _thread
import pickle
import socket
import time
import tkinter as tk
from random import randint
from tkinter import messagebox
import pygame
from data.constants import *


class Player:
    """A class that represents players for the game, and so has all neccessary attributes"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0


class Game:
    """A class used during the playing of 'duo game'. Online game's class is stored in a separate file, so the server can access it independently"""

    def __init__(self):
        self.round = 0
        self.turn = player_one


class PlayerOneLoginPage(tk.Frame):
    """A class used to create the login page for the first player. It inherits from tk.Frame, so that it can be used as one"""

    def __init__(self, master):
        self.master = master

        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])
        self.pack_propagate(0)
        self.alert_made = False

        self.login_label = tk.Label(self, text="Login", font=(FONT, TITLE_FONT_SIZE),
                                    fg=master.font_colour, bg=master.colour[1]).pack(pady=30)
        self.username_label = tk.Label(self, text="Username: ", bg=master.colour[1], fg=master.font_colour).pack(
            pady=10)
        self.username_entry = tk.Entry(self, bg=master.colour[1], fg=master.font_colour, borderwidth=1, relief="flat")
        self.username_entry.pack(pady=10)
        self.password_label = tk.Label(self, text="Password:", bg=master.colour[1], fg=master.font_colour).pack(pady=10)
        self.password_entry = tk.Entry(self, bg=master.colour[1], show="*", fg=master.font_colour, borderwidth=1,
                                       relief="flat")
        self.password_entry.pack(pady=10)
        self.login_button = tk.Button(self, text="Confirm", bg=master.colour[1], highlightbackground=master.colour[1],
                                      command=lambda: self.check_login(self.username_entry.get(),
                                                                       self.password_entry.get())).pack(pady=20)
        self.create_account_label = tk.Label(self, text="Don't have an account?\n\nCreate an account:",
                                             bg=master.colour[1], fg=master.font_colour).pack(pady=30)
        self.create_account_button = tk.Button(self, text="Confirm", bg=master.colour[1],
                                               highlightbackground=master.colour[1],
                                               command=lambda: self.master.switch_frame(PlayerOneCreateAccountPage)
                                               ).pack(pady=10)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def check_login(self, username, password):
        """A method used as a form of validation to make sure the users details are correct, when they try to log in"""
        global player_one
        found = False
        with open(LOGINS_FILE, "r") as f:
            for x in f:
                if x.split(" ")[0] == username and x.split(" ")[1] == password:
                    found = True
                    colour = x.split(" ")[2]
                    volume = x.split(" ")[3]

        if found:
            player_one = Player(username, password)
            self.master.colour = self.master.colours_dict[f"{colour}"][0]
            self.master.font_colour = self.master.colours_dict[f"{colour}"][1]
            self.master.dice = self.master.colours_dict[f"{colour}"][2]
            self.master.configure(bg=self.master.colours_dict[f"{colour}"][0][0])
            pygame.mixer.music.set_volume(float(volume))
            self.master.switch_frame(GameMenu)

        elif not self.alert_made:
            alert_label = tk.Label(self,
                                   text="Sorry, the username or password you entered was incorrect."
                                        "\nPlease try again.",
                                   fg="orange", bg=self.master.colour[1]).pack()
            self.alert_made = True


class PlayerOneCreateAccountPage(tk.Frame):
    """A class used to create a page that allows player one to create a new account"""

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])

        self.pack_propagate(0)

        self.alert_made = False

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: self.master.switch_frame(PlayerOneLoginPage)).pack(anchor="nw",
                                                                                                        padx=5, pady=5)
        self.create_account_label = tk.Label(self, text="Create Account", font=(FONT, TITLE_FONT_SIZE),
                                             bg=self.master.colour[1], fg=self.master.font_colour).pack()
        self.username_label = tk.Label(self, text="New Username: ", bg=self.master.colour[1],
                                       fg=self.master.font_colour).pack(pady=20)
        self.username_entry = tk.Entry(self, bg=self.master.colour[1], fg=self.master.font_colour, borderwidth=1,
                                       relief="flat")
        self.username_entry.pack(pady=20)
        self.password_label = tk.Label(self, text="New Password: ", bg=self.master.colour[1],
                                       fg=self.master.font_colour).pack(pady=20)
        self.password_entry = tk.Entry(self, bg=self.master.colour[1], show="*",
                                       fg=self.master.font_colour, borderwidth=1, relief="flat")
        self.password_entry.pack(pady=20)
        self.confirm_password_label = tk.Label(self, text="Confirm New Password: ", bg=self.master.colour[1],
                                               fg=self.master.font_colour).pack(pady=20)
        self.confirm_password_entry = tk.Entry(self, bg=self.master.colour[1], show="*",
                                               fg=self.master.font_colour, borderwidth=1, relief="flat")
        self.confirm_password_entry.pack(pady=20)
        self.confirm_create_account_button = tk.Button(self, text="Confirm", bg=self.master.colour[1],
                                                       highlightbackground=self.master.colour[1],
                                                       command=lambda: self.confirm_new_account(
                                                           self.username_entry.get(), self.password_entry.get(),
                                                           self.confirm_password_entry.get())).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def confirm_new_account(self, username, password, confirm_password):
        """Like the method in the previous class, this checks player one's details to ensure that they are of a certain
        length, and do not use a username owned by another player in the logins file"""
        global player_one

        with open(LOGINS_FILE, "r") as f:
            for x in f:
                found = True if x.split(" ")[0] == username else False

        valid = True if 2 < len(username) < 15 and 2 < len(password) < 15 else False

        with open(LOGINS_FILE, "a+") as f:

            if not found and password == confirm_password and valid:
                f.write(f"\n{username} {password} blue 0.2")
                player_one = Player(username, password)
                self.master.switch_frame(GameMenu)

            elif not self.alert_made:
                alert_label = tk.Label(self,
                                       text="Sorry, the input you entered was invalid\nPlease try again.", fg="orange",
                                       bg=self.master.colour[1]).pack()
                self.alert_made = True


class GameMenu(tk.Frame):
    "A class used to display the main menu page of the game to the root window(tk.Tk()), contains mainly widget instances, such a button and entries"

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])
        self.pack_propagate(0)

        master.title(f"Game Menu - {player_one.username}")

        self.game_menu_label = tk.Label(self, text="Game Menu", font=(FONT, TITLE_FONT_SIZE),
                                        fg=self.master.font_colour, bg=self.master.colour[1]).pack(pady=60)
        self.play_duo_button = tk.Button(self, text="Duo Game", bg=self.master.colour[1],
                                         highlightbackground=self.master.colour[1], width=25, height=2,
                                         command=lambda: self.master.switch_frame(PlayerTwoLoginPage)).pack(pady=20)
        self.play_online_button = tk.Button(self, text="Online Game", bg=self.master.colour[1],
                                            highlightbackgroun=self.master.colour[1], width=25,
                                            height=2,
                                            command=lambda: self.master.switch_frame(OnlineGameInitPage)).pack(
            pady=20)
        self.rules_button = tk.Button(self, text="Rules", bg=self.master.colour[1],
                                      highlightbackground=self.master.colour[1], width=25, height=2,
                                      command=lambda: self.master.switch_frame(Rules)).pack(pady=20)
        self.settings_button = tk.Button(self, text="Settings", bg=self.master.colour[1],
                                         highlightbackground=self.master.colour[1], width=25, height=2,
                                         command=lambda: self.master.switch_frame(Settings)).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")


class Settings(tk.Frame):
    """A class that allows for the creation of the settings, page as it inherits from tk.Frame"""
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])
        self.pack_propagate(0)

        master.title(f"Settings - {player_one.username}")

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: self.master.switch_frame(GameMenu))
        self.back_button.pack(anchor="nw",
                              padx=5, pady=5)
        self.game_menu_label = tk.Label(self, text="Settings", font=(FONT, TITLE_FONT_SIZE),
                                        fg=self.master.font_colour, bg=self.master.colour[1]).pack(pady=30)
        self.music_title_label = tk.Label(self, text="Music", font=(FONT, 25, "underline"), fg=self.master.font_colour,
                                          bg=self.master.colour[1]).pack(pady=10)
        self.music_volume_label = tk.Label(self, text="Music Volume: ", fg=self.master.font_colour,
                                           bg=self.master.colour[1]).pack(pady=10)
        self.music_volume_scale = tk.Scale(self, orient="horizontal", bg=self.master.colour[1], fg=master.font_colour,
                                           length=80, troughcolor=self.master.colour[1], showvalue=0,
                                           highlightcolor=self.master.colour[1],
                                           highlightbackground=self.master.colour[1],
                                           activebackground=self.master.colour[1], command=self.change_volume)
        self.music_volume_scale.set(pygame.mixer.music.get_volume() * 100)
        self.music_volume_scale.pack(pady=10)
        self.themes_title_label = tk.Label(self, text="Themes", font=(FONT, 25, "underline"),
                                           fg=self.master.font_colour, bg=self.master.colour[1]).pack(pady=10)
        self.blue_theme_checkbox = tk.Checkbutton(self, text="Blue", bg=self.master.colour[1],
                                                  fg=self.master.font_colour)
        self.blue_theme_checkbox.pack(pady=10)
        self.green_theme_checkbox = tk.Checkbutton(self, text="Green", bg=self.master.colour[1],
                                                   fg=self.master.font_colour)
        self.green_theme_checkbox.pack(pady=10)
        self.black_theme_checkbox = tk.Checkbutton(self, text="Dark", bg=self.master.colour[1],
                                                   fg=self.master.font_colour)
        self.black_theme_checkbox.pack(pady=10)

        self.white_theme_checkbox = tk.Checkbutton(self, text="Light", bg=self.master.colour[1],
                                                   fg=self.master.font_colour)
        self.white_theme_checkbox.pack(pady=10)

        self.blue_theme_checkbox.configure(command=lambda: self.change_theme("blue", self.blue_theme_checkbox))
        self.green_theme_checkbox.configure(command=lambda: self.change_theme("green", self.green_theme_checkbox))
        self.black_theme_checkbox.configure(command=lambda: self.change_theme("black", self.black_theme_checkbox))
        self.white_theme_checkbox.configure(command=lambda: self.change_theme("white", self.white_theme_checkbox))

        self.log_out_button = tk.Button(self, text="Log Out", bg=self.master.colour[1],
                                        highlightbackground=self.master.colour[1],
                                        command=lambda: self.log_out())
        self.log_out_button.pack(anchor="se", padx=5)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")

        self.blue_theme_checkbox.deselect()
        self.green_theme_checkbox.deselect()
        self.black_theme_checkbox.deselect()
        self.white_theme_checkbox.deselect()

        if self.master.colour == BLUE:
            self.blue_theme_checkbox.select()
        elif self.master.colour == GREEN:
            self.green_theme_checkbox.select()
        elif self.master.colour == BLACK:
            self.black_theme_checkbox.select()
        elif self.master.colour == WHITE:
            self.white_theme_checkbox.select()

    def change_theme(self, theme, button):
        self.blue_theme_checkbox.deselect()
        self.green_theme_checkbox.deselect()
        self.black_theme_checkbox.deselect()
        self.white_theme_checkbox.deselect()
        button.select()

        if self.master.colour == BLUE:
            current_colour = "blue"
        elif self.master.colour == GREEN:
            current_colour = "green"
        elif self.master.colour == BLACK:
            current_colour = "black"
        elif self.master.colour == WHITE:
            current_colour = "white"

        with open(LOGINS_FILE, 'r+') as f:
            contents = f.read().replace(f"{player_one.username} {player_one.password} {str(current_colour).lower()}",
                                        f"{player_one.username} {player_one.password} {theme}")
        with open(LOGINS_FILE, 'w+') as f:

            f.write(contents)

        self.master.colour = self.master.colours_dict[f"{theme}"][0]
        self.master.font_colour = self.master.colours_dict[f"{theme}"][1]
        self.master.dice = self.master.colours_dict[f"{theme}"][2]
        self.master.configure(bg=self.master.colours_dict[f"{theme}"][0][0])
        self.configure(bg=self.master.colour[1])

        for i in self.pack_slaves():
            i.configure(bg=self.master.colour[1], highlightbackground=self.master.colour[1], fg=self.master.font_colour)

        self.music_volume_scale.configure(troughcolor=self.master.colour[1], activebackground=self.master.colour[1])
        self.back_button.configure(fg="black")
        self.log_out_button.configure(fg="black")

    def change_volume(self, volume):

        if self.master.colour == BLUE:
            current_colour = "blue"
        elif self.master.colour == GREEN:
            current_colour = "green"
        elif self.master.colour == BLACK:
            current_colour = "green"
        elif self.master.colour == WHITE:
            current_colour = "white"

        with open(LOGINS_FILE) as f:
            contents = f.read().replace(
                f"{player_one.username} {player_one.password} {str(current_colour).lower()} {round(pygame.mixer.music.get_volume(), 1)}",
                f"{player_one.username} {player_one.password} {str(current_colour).lower()} {round((float(volume) / 100), 1)}")
        with open(LOGINS_FILE, 'w+') as f:
            f.write(contents)

        pygame.mixer.music.set_volume(float(int(volume) / 100))

    def log_out(self):

        self.log_out_messagebox = messagebox.askokcancel(title='Confirm',
                                                         message='Are you sure you want to log out?')
        if self.log_out_messagebox:
            player_one.username = ""
            player_one.password = ""
            self.master.colour = BLUE
            self.master.font_colour = "white"
            self.master.colours_dict = {"blue": [BLUE, "white", BLUE_DICE], "green": [GREEN, "white", GREEN_DICE],
                                        "black": [BLACK, "white", BLACK_DICE],
                                        "white": [WHITE, "black", WHITE_DICE]}

            self.master.dice = BLUE_DICE
            self.configure(bg=self.master.colour[1])
            self.master.configure(bg=self.master.colour[0])
            pygame.mixer.music.set_volume(0.2)

            self.master.switch_frame(PlayerOneLoginPage)


class Rules(tk.Frame):
    """A class that creates the rules page, shows the rules for the game on screen"""
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])
        self.pack_propagate(0)

        self.master.title(f"Rules - {player_one.username}")

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: master.switch_frame(GameMenu)).pack(anchor="nw", padx=5, pady=5)

        self.rules_title_label = tk.Label(self, text="Rules", font=(FONT, 30),
                                          fg=self.master.font_colour, bg=self.master.colour[1]).pack(pady=40)

        self.rules_label = tk.Label(self,
                                    text='- In the dice game there are two dice, one belonging to each player.\n\n- Each player takes turns to roll their dice, once you receive a roll,\n\ndifferent points will be added and subtracted depending on its nature.\n\n- If a player rolls an even number, 10 points are added to their score.\n\n- If a player rolls an odd number, then 5 points are subtracted from their score,\n\nunless it would cause their score to become negative.\n\n- If a player rolls a double, they receive an additional roll.\n\n- There are five rounds, where each rounds of each player rolling their dice once.\n\n- If both players scores are the same at the end of the five rounds,\n\nthen additional rounds will commence until the scores are no longer the same. ',
                                    bg=self.master.colour[1], fg=self.master.font_colour).pack(pady=10)

        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=self.master.colour[1],
                                        fg=self.master.font_colour, font=(None, 10)).pack(side="bottom")


class PlayerTwoLoginPage(tk.Frame):
    """A class that allows player two to login and play the duo game"""
    def __init__(self, master):
        self.master = master

        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])

        master.title(f"Player Two Login - {player_one.username}")

        self.pack_propagate(0)
        self.alert_made = False

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: self.master.switch_frame(GameMenu)).pack(anchor="nw",
                                                                                              padx=5, pady=5)
        self.player_two_login_label = tk.Label(self, text="Player Two Login", font=(FONT, TITLE_FONT_SIZE),
                                               fg=master.font_colour, bg=master.colour[1]).pack(pady=5)
        self.info_label = tk.Label(self, text="Information: you will be logged out\n at the end of the game.",
                                   bg=master.colour[1], fg=master.font_colour).pack(pady=5)
        self.username_label = tk.Label(self, text="Username: ", bg=master.colour[1], fg=master.font_colour).pack(
            pady=10)
        self.username_entry = tk.Entry(self, bg=master.colour[1], fg=master.font_colour, borderwidth=1, relief="flat")
        self.username_entry.pack(pady=10)
        self.password_label = tk.Label(self, text="Password:", bg=master.colour[1], fg=master.font_colour).pack(pady=5)
        self.password_entry = tk.Entry(self, bg=master.colour[1], show="*", fg=master.font_colour, borderwidth=1,
                                       relief="flat")
        self.password_entry.pack(pady=10)
        self.login_button = tk.Button(self, text="Confirm", bg=master.colour[1], highlightbackground=master.colour[1],
                                      command=lambda: self.check_login(self.username_entry.get(),
                                                                       self.password_entry.get())).pack(pady=20)
        self.create_account_label = tk.Label(self, text="Don't have an account?\n\nCreate an account:",
                                             bg=master.colour[1], fg=master.font_colour).pack(pady=10)
        self.create_account_button = tk.Button(self, text="Confirm", bg=master.colour[1],
                                               highlightbackground=master.colour[1],
                                               command=lambda: self.master.switch_frame(PlayerTwoCreateAccountPage)
                                               ).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def check_login(self, username, password):
        global player_two
        found = False
        with open(LOGINS_FILE, "r") as f:
            for x in f:
                if x.split(" ")[0] == username and x.split(" ")[1] == password:
                    found = True
                    colour = x.split(" ")[2]
                    volume = x.split(" ")[3]

        if found:
            player_two = Player(username, password)
            self.master.switch_frame(DuoGame)

        elif not self.alert_made:
            alert_label = tk.Label(self,
                                   text="Sorry, the username or password you entered were incorrect."
                                        "\nPlease try again.",
                                   fg="orange", bg=self.master.colour[1]).pack()
            self.alert_made = True


class PlayerTwoCreateAccountPage(tk.Frame):
    "A class that allows player two to optionally create a page, if they cannot don't wont to login"
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])

        self.pack_propagate(0)
        master.title(f"Player Two Create Account - {player_one.username}")

        self.alert_made = False

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: self.master.switch_frame(PlayerTwoLoginPage)).pack(anchor="nw",
                                                                                                        padx=5, pady=5)
        self.create_account_label = tk.Label(self, text="Create Account", font=(FONT, TITLE_FONT_SIZE),
                                             bg=self.master.colour[1], fg=self.master.font_colour).pack()
        self.info_label = tk.Label(self, text="Information: you will be logged out\n at the end of the game.",
                                   bg=master.colour[1], fg=master.font_colour).pack(pady=15)
        self.username_label = tk.Label(self, text="New Username: ", bg=self.master.colour[1],
                                       fg=self.master.font_colour).pack(pady=10)
        self.username_entry = tk.Entry(self, bg=self.master.colour[1], fg=self.master.font_colour, borderwidth=1,
                                       relief="flat")
        self.username_entry.pack(pady=10)
        self.password_label = tk.Label(self, text="New Password: ", bg=self.master.colour[1],
                                       fg=self.master.font_colour).pack(pady=10)
        self.password_entry = tk.Entry(self, bg=self.master.colour[1], show="*",
                                       fg=self.master.font_colour, borderwidth=1, relief="flat")
        self.password_entry.pack(pady=10)
        self.confirm_password_label = tk.Label(self, text="Confirm New Password: ", bg=self.master.colour[1],
                                               fg=self.master.font_colour).pack(pady=10)
        self.confirm_password_entry = tk.Entry(self, bg=self.master.colour[1], show="*",
                                               fg=self.master.font_colour, borderwidth=1, relief="flat")
        self.confirm_password_entry.pack(pady=10)
        self.confirm_create_account_button = tk.Button(self, text="Confirm", bg=self.master.colour[1],
                                                       highlightbackground=self.master.colour[1],
                                                       command=lambda: self.confirm_new_account(
                                                           self.username_entry.get(), self.password_entry.get(),
                                                           self.confirm_password_entry.get())).pack(pady=30)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def confirm_new_account(self, username, password, confirm_password):
        """A function that checks player two's credentials are valid, if they are a new account will be made"""
        global player_two

        with open(LOGINS_FILE, "r") as f:
            for x in f:
                found = True if x.split(" ")[0] == username else False

        valid = True if 2 < len(username) < 15 and 2 < len(password) < 15 else False

        with open(LOGINS_FILE, "a+") as f:

            if not found and password == confirm_password and valid:
                f.write(f"\n{username} {password} blue 0.2")
                player_two = Player(username, password)
                self.master.switch_frame(DuoGame)

            elif not self.alert_made:
                alert_label = tk.Label(self,
                                       text="Sorry, the input you entered was invalid\nPlease try again.", fg="orange",
                                       bg=self.master.colour[1]).pack()
                self.alert_made = True


class DuoGame(tk.Frame):
    "A class that creates an instance of the duo game"
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[0])
        self.pack_propagate(0)

        master.title(f"Duo Game - {player_one.username} vs {player_two.username}")

        self.game = Game()

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[0],
                                     highlightbackground=self.master.colour[0], command=lambda: self.quit_game()).pack(
            anchor="nw", padx=5, pady=5)

        self.title = tk.Label(self, text="Duo Game", bg=self.master.colour[0], fg=self.master.font_colour,
                              font=(FONT, 30))
        self.title.grid(column=0, row=0, columnspan=3, pady=4)

        self.player_one_title = tk.Label(self, text="Player One: \n " + player_one.username, bg=self.master.colour[0],
                                         fg=self.master.font_colour,
                                         width=10)
        self.player_one_title.grid(column=0, row=1, sticky="N")

        self.player_score_title = tk.Label(self, text="Round: " + str(self.game.round) + "\n\nScore:\n" + str(
            player_one.score) + " : " + str(player_two.score),
                                           bg=self.master.colour[0], fg=self.master.font_colour, width=10)
        self.player_score_title.grid(column=1, row=1, sticky="N")

        self.player_two_title = tk.Label(self, text="Player Two: \n" + player_two.username, bg=self.master.colour[0],
                                         fg=self.master.font_colour,
                                         width=10)
        self.player_two_title.grid(column=2, row=1, sticky="N")

        self.player_one_frame = tk.Frame(self, bg=self.master.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_one_frame.grid(column=0, row=2, sticky="N", padx=5)

        self.player_one_frame.pack_propagate(0)

        self.border_frame = tk.Frame(self, bg=self.master.colour[0], width=WINDOW_WIDTH / 100 * 2)
        self.border_frame.grid(column=1, row=2)

        self.player_two_frame = tk.Frame(self, bg=self.master.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_two_frame.grid(column=2, row=2, sticky="N", padx=5)

        self.player_two_frame.pack_propagate(0)

        self.player_one_dice_image_one = tk.Label(self.player_one_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_one_dice_image_one.pack(pady=5, side="top")

        self.player_one_dice_image_two = tk.Label(self.player_one_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_one_dice_image_two.pack(pady=5, side="top")

        self.player_one_calc_box = tk.Label(self.player_one_frame, text="Result:\nNothing", bg=self.master.colour[1],
                                            fg=self.master.font_colour,
                                            width=50, height=5)
        self.player_one_calc_box.pack(pady=10)

        self.player_two_dice_image_one = tk.Label(self.player_two_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_two_dice_image_one.pack(pady=5, side="top")

        self.player_two_dice_image_two = tk.Label(self.player_two_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_two_dice_image_two.pack(pady=5, side="top")

        self.player_two_calc_box = tk.Label(self.player_two_frame, text="Result:\nNothing", bg=self.master.colour[1],
                                            fg=self.master.font_colour,
                                            width=50, height=5)
        self.player_two_calc_box.pack(pady=10)

        self.player_one_roll_button = tk.Button(self.player_one_frame, text="ROLL!", bg=self.master.colour[1],
                                                highlightbackground=self.master.colour[1],
                                                command=lambda: self.roll(player_one))
        self.player_one_roll_button.pack()

        self.player_one_info = tk.Label(self.player_one_frame, text="OR Press Left Shift!", bg=self.master.colour[1],
                                        fg=self.master.font_colour,
                                        height=5).pack(pady=10)

        self.player_two_roll_button = tk.Button(self.player_two_frame, text="ROLL!", bg=self.master.colour[1],
                                                highlightbackground=self.master.colour[1],
                                                command=lambda: self.roll(player_two))
        self.player_two_roll_button.pack()

        self.player_two_tip = tk.Label(self.player_two_frame, text="OR Press Return!", bg=self.master.colour[1],
                                       fg=self.master.font_colour,
                                       height=5).pack(pady=10)

        self.player_two_roll_button["state"] = "disabled"

        self.master.bind("<Key-Shift_L>", lambda event: self.roll(player_one))
        self.master.bind("<Key-Return>", lambda event: self.roll(player_two))

    def roll(self, player):

        if self.game.round <= 5 or player_one.score == player_two.score:
            if player == player_one and self.game.turn == player_one:
                player.roll_1 = randint(1, 6)
                player.roll_2 = randint(1, 6)
                player.round_score = player.roll_1 + player.roll_2
                player.roll_again = False

                self.player_one_dice_image_one.configure(image=self.master.dice[player.roll_1 - 1])
                self.player_one_dice_image_two.configure(image=self.master.dice[player.roll_2 - 1])

                player.calc_result = ""

                if player.roll_1 == player.roll_2:
                    player.calc_result += "You rolled a double, so you get an additional roll.\n"
                    player.roll_again = True

                if (player.roll_1 + player.roll_2) % 2 == 0:
                    player.calc_result += "You rolled an even number.\nYour roll gains 10 points."
                    player.round_score += 10

                else:
                    player.calc_result += "You rolled an odd number.\nYour roll loses 5 points."
                    player.round_score -= 5

                if player.round_score < 0:
                    player.round_score = 0

                player.score += player.round_score
                self.player_one_calc_box.configure(text=str(player.calc_result))
                player.round_score = 0

                if not player.roll_again:
                    self.player_two_roll_button["state"] = "normal"
                    self.player_one_roll_button["state"] = "disabled"
                    self.game.turn = player_two

                self.player_score_title.configure(
                    text="Round: " + str(self.game.round) + "\n\nScore\n" + str(player_one.score) + ":" + str(
                        player_two.score))

            elif player == player_two and self.game.turn == player_two:
                player.roll_1 = randint(1, 6)
                player.roll_2 = randint(1, 6)
                player.round_score = player.roll_1 + player.roll_2
                player.roll_again = False

                self.player_two_dice_image_one.configure(image=self.master.dice[player.roll_1 - 1])
                self.player_two_dice_image_two.configure(image=self.master.dice[player.roll_2 - 1])

                player.calc_result = "Result:\n"

                if player.roll_1 == player.roll_2:
                    player.calc_result += "You rolled a double, so you get an additional roll.\n"
                    player.roll_again = True

                else:
                    pass

                if (player.roll_1 + player.roll_2) % 2 == 0:
                    player.calc_result += "You rolled an even number.\nYour roll gains 10 points."

                    player.round_score += 10


                else:
                    player.calc_result += "You rolled an odd number.\nYour roll loses 5 points."
                    player.round_score -= 5

                if player.round_score < 0:
                    player.round_score = 0

                player.score += player.round_score
                self.player_two_calc_box.configure(text=str(player.calc_result))
                player.round_score = 0

                if not player.roll_again:
                    self.player_two_roll_button["state"] = "disabled"
                    self.player_one_roll_button["state"] = "active"
                    self.game.round += 1
                    self.game.turn = player_one

                self.player_score_title.configure(
                    text="Round: " + str(self.game.round) + "\n\nScore\n" + str(player_one.score) + ":" + str(
                        player_two.score))

        else:

            self.master.switch_frame(GameOverFrame)

    def quit_game(self):

        self.quit_messagebox = messagebox.askokcancel(title='Confirm',
                                                      message='Are you sure you want to quit?\nGame progress will not be saved!')
        if self.quit_messagebox:
            self.master.switch_frame(GameMenu)


class GameOverFrame(tk.Frame):
    """A class that shows the results of the game including the players highscores"""
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])
        self.pack_propagate(0)

        master.title(f"Game Over")

        master.unbind("<Key-Shift_L>")
        master.unbind("<Key-Return>")

        with open(HIGH_SCORES_FILE, 'a+') as f:
            f.write(f"{player_one.username} {player_one.score}\n{player_two.username} {player_two.score}\n")

        with open(HIGH_SCORES_FILE, 'r') as f:
            result = ""
            players_and_scores = f.read().split("\n")
            players_and_scores.pop(-1)
            players_and_scores = sorted(players_and_scores, key=lambda score: int(score.split(' ')[1]), reverse=True)

            if len(players_and_scores) >= 10:
                for i in range(10):
                    result += f"{players_and_scores[i].split(' ')[0]}: {players_and_scores[i].split(' ')[1]}\n"
            else:
                result = "Sorry, there are not enough scores to show."

        winner = f"{player_one.username}" if player_one.score > player_two.score else f"{player_two.username}"

        self.results = tk.Label(self,
                                text="Congratulations " + str(winner) + ", you won!\n\nThe final score was: " + str(
                                    player_one.score) + "-" + str(
                                    player_two.score) + ".\n\nAll scores will be saved in a file, and you can see the top 10 high scores below:",
                                bg=self.master.colour[1], fg=self.master.font_colour).pack(pady=40)

        self.high_scores_label = tk.Label(self, text=f"{result}", bg=self.master.colour[1],
                                          fg=self.master.font_colour).pack(pady=20)

        self.main_menu_button = tk.Button(self, text="Main Menu", bg=self.master.colour[1],
                                          highlightbackground=self.master.colour[1],
                                          command=lambda: master.switch_frame(GameMenu)).pack(pady=50)

        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=self.master.colour[1],
                                        fg=self.master.font_colour, font=(None, 10)).pack(side="bottom")


class OnlineGameInitPage(tk.Frame):
    "A class that creates a page that asks for the details required for the online game"
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])

        self.pack_propagate(0)

        self.master.title(f"Online Game - {player_one.username}")

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: master.switch_frame(GameMenu)).pack(anchor="nw", padx=5, pady=5)
        self.online_game_title_label = tk.Label(self, text="Online Game", font=(FONT, 30),
                                                fg=self.master.font_colour, bg=self.master.colour[1]).pack(pady=20)
        self.online_game_info_label = tk.Label(self,
                                               text="Hi, welcome to online game!\nOnline game is just like duo game,  except\nyou play against people over a network\ninstead of on a single machine.\nHave fun!",
                                               fg=self.master.font_colour, bg=self.master.colour[1]).pack(pady=20)
        self.server_ip_label = tk.Label(self, text="Server IP:\n\ne.g. 192.168.1.1", fg=self.master.font_colour,
                                        bg=self.master.colour[1]).pack(pady=20)
        self.server_ip_entry = tk.Entry(self, fg=self.master.font_colour,
                                        bg=self.master.colour[1])
        self.server_ip_entry.pack(pady=20)
        self.play_button = tk.Button(self, text="Play", fg="black", width=5, bg=self.master.colour[1],
                                     highlightbackground=self.master.colour[1],
                                     command=lambda: self.master.switch_frame(OnlineGamePage,
                                                                              self.server_ip_entry.get())).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=master.colour[1], fg=master.font_colour,
                                        font=(None, 10)).pack(side="bottom")


class OnlineGamePage(tk.Frame):
    "A page that creates an instance of the online game"
    def __init__(self, master, server_ip):
        self.master = master
        self.server_ip = server_ip
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[0])
        self.pack_propagate(0)

        master.title(f"Game Over")

        self.back_button = tk.Button(self, text="back", bg=self.master.colour[0],
                                     highlightbackground=self.master.colour[0],
                                     command=lambda: self.master.switch_frame(GameMenu)).pack(
            anchor="nw", padx=5, pady=5)

        self.title = tk.Label(self, text="Online Game", bg=self.master.colour[0], fg=self.master.font_colour,
                              font=(FONT, 30))
        self.title.grid(column=0, row=0, columnspan=3, pady=4)

        self.player_one_title = tk.Label(self, text="Player One: \n " + player_one.username, bg=self.master.colour[0],
                                         fg=self.master.font_colour,
                                         width=10)
        self.player_one_title.grid(column=0, row=1, sticky="N")

        self.player_score_title = tk.Label(self, text=f"Round: 0\n\nScore:\n0:0", bg=self.master.colour[0],
                                           fg=self.master.font_colour, width=10)
        self.player_score_title.grid(column=1, row=1, sticky="N")

        self.player_two_title = tk.Label(self, text="Player Two:\n Waiting...", bg=self.master.colour[0],
                                         fg=self.master.font_colour,
                                         width=20)
        self.player_two_title.grid(column=2, row=1, sticky="N")

        self.player_one_frame = tk.Frame(self, bg=self.master.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_one_frame.grid(column=0, row=2, sticky="N", padx=5)

        self.player_one_frame.pack_propagate(0)

        self.border_frame = tk.Frame(self, bg=self.master.colour[0], width=WINDOW_WIDTH / 100 * 2)
        self.border_frame.grid(column=1, row=2)

        self.player_two_frame = tk.Frame(self, bg=self.master.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_two_frame.grid(column=2, row=2, sticky="N", padx=5)

        self.player_two_frame.pack_propagate(0)

        self.player_one_dice_image_one = tk.Label(self.player_one_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_one_dice_image_one.pack(pady=5, side="top")

        self.player_one_dice_image_two = tk.Label(self.player_one_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_one_dice_image_two.pack(pady=5, side="top")

        self.player_one_calc_box = tk.Label(self.player_one_frame, text="Result:\nNothing", bg=self.master.colour[1],
                                            fg=self.master.font_colour,
                                            width=50, height=5)
        self.player_one_calc_box.pack(pady=10)

        self.player_two_dice_image_one = tk.Label(self.player_two_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_two_dice_image_one.pack(pady=5, side="top")

        self.player_two_dice_image_two = tk.Label(self.player_two_frame, bg=self.master.colour[1],
                                                  image=self.master.dice[5])
        self.player_two_dice_image_two.pack(pady=5, side="top")

        self.player_two_calc_box = tk.Label(self.player_two_frame, text="Result:\nNothing", bg=self.master.colour[1],
                                            fg=self.master.font_colour,
                                            width=50, height=5)
        self.player_two_calc_box.pack(pady=10)

        self.player_one_roll_button = tk.Button(self.player_one_frame, text="ROLL!", bg=self.master.colour[1],
                                                highlightbackground=self.master.colour[1],
                                                command=lambda: self.roll(self.actual_player_no))
        self.player_one_roll_button.pack()
        self.player_one_roll_button['state'] = 'disabled'

        self.player_one_info = tk.Label(self.player_one_frame, text="OR Press Left Shift!", bg=self.master.colour[1],
                                        fg=self.master.font_colour,
                                        height=5).pack(pady=10)

        self.master.bind("<Key-Shift_L>", lambda event: self.roll(self.actual_player_no))

        _thread.start_new_thread(self.network, (str(self.server_ip), 65432))

    def network(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            try:
                self.s.connect((host, port))

                self.actual_player_no = int(self.s.recv(2048).decode())
                self.s.sendall(str.encode(player_one.username))
                while True:
                    time.sleep(0.1)
                    try:
                        self.game_obj = pickle.loads(self.s.recv(2048))

                        if self.game_obj.ready:

                            if self.game_obj.round_no < 6:

                                if self.actual_player_no == 0:
                                    self.player_two_dice_image_one.configure(
                                        image=self.master.dice[self.game_obj.player_two_roll_one - 1])
                                    self.player_two_dice_image_two.configure(
                                        image=self.master.dice[self.game_obj.player_two_roll_two - 1])

                                    self.game_obj.player_one_name = player_one.username
                                    self.player_two_title.configure(
                                        text=f"Player Two:\n{self.game_obj.player_two_name}")
                                    self.player_score_title.configure(
                                        text=f"Round: {self.game_obj.round_no}\n\nScore:\n{self.game_obj.player_one_score}:{self.game_obj.player_two_score}")

                                    if self.game_obj.player_turn == 0:
                                        self.player_one_roll_button["state"] = "normal"

                                    else:
                                        self.player_one_roll_button["state"] = "disabled"
                                        self.s.sendall(pickle.dumps(self.game_obj))

                                elif self.actual_player_no == 1:
                                    self.player_two_dice_image_one.configure(
                                        image=self.master.dice[self.game_obj.player_one_roll_one - 1])
                                    self.player_two_dice_image_two.configure(
                                        image=self.master.dice[self.game_obj.player_one_roll_two - 1])

                                    self.game_obj.player_two_name = player_one.username
                                    self.player_two_title.configure(
                                        text=f"Player Two:\n{self.game_obj.player_one_name}")
                                    self.player_score_title.configure(
                                        text=f"Round: {self.game_obj.round_no}\n\nScore:\n{self.game_obj.player_two_score}:{self.game_obj.player_one_score}")
                                    if self.game_obj.player_turn == 1:
                                        self.player_one_roll_button["state"] = "normal"

                                    else:
                                        self.player_one_roll_button["state"] = "disabled"
                                        self.s.sendall(pickle.dumps(self.game_obj))

                            else:
                                if self.actual_player_no == 0:
                                    self.master.switch_frame(GameOverFrameOnline, self.game_obj.player_one_score,
                                                             self.game_obj.player_two_name,
                                                             self.game_obj.player_two_score)
                                elif self.actual_player_no == 1:
                                    self.master.switch_frame(GameOverFrameOnline, self.game_obj.player_two_score,
                                                             self.game_obj.player_one_name,
                                                             self.game_obj.player_one_score)

                        else:
                            self.s.sendall(pickle.dumps(self.game_obj))

                    except:
                        pass

            except:
                self.could_not_connect_messagebox = messagebox.showerror(title="Error",
                                                                         message="Could not connect to the server IP entered.")
                if self.could_not_connect_messagebox:
                    self.master.switch_frame(OnlineGameInitPage)

    def roll(self, player):
        if player == 0 and self.game_obj.player_turn == 0:
            self.game_obj.player_one_roll_one = randint(1, 6)
            self.game_obj.player_one_roll_two = randint(1, 6)
            self.player_one_round_score = self.game_obj.player_one_roll_one + self.game_obj.player_one_roll_two
            self.player_one_roll_again = False

            self.player_one_dice_image_one.configure(image=self.master.dice[self.game_obj.player_one_roll_one - 1])
            self.player_one_dice_image_two.configure(image=self.master.dice[self.game_obj.player_one_roll_two - 1])

            self.player_one_calc_result = ""

            if self.game_obj.player_one_roll_one == self.game_obj.player_one_roll_two:
                self.player_one_calc_result += "You rolled a double, so you get an additional roll.\n"
                self.player_one_roll_again = True

            if (self.game_obj.player_one_roll_one + self.game_obj.player_one_roll_two) % 2 == 0:
                self.player_one_calc_result += "You rolled an even number.\nYour roll gains 10 points."
                self.player_one_round_score += 10

            else:
                self.player_one_calc_result += "You rolled an odd number.\nYour roll loses 5 points."
                self.player_one_round_score -= 5

            if self.player_one_round_score < 0:
                self.player_one_round_score = 0

            self.game_obj.player_one_score += self.player_one_round_score
            self.player_one_calc_box.configure(text=str(self.player_one_calc_result))
            self.player_one_round_score = 0

            if not self.player_one_roll_again:
                self.player_one_roll_button["state"] = "disabled"
                self.game_obj.player_turn = int(not (self.game_obj.player_turn))
                self.s.sendall(pickle.dumps(self.game_obj))

        elif player == 1 and self.game_obj.player_turn == 1:

            self.game_obj.player_two_roll_one = randint(1, 6)
            self.game_obj.player_two_roll_two = randint(1, 6)
            self.player_one_round_score = self.game_obj.player_two_roll_one + self.game_obj.player_two_roll_two
            self.player_one_roll_again = False

            self.player_one_dice_image_one.configure(image=self.master.dice[self.game_obj.player_two_roll_one - 1])
            self.player_one_dice_image_two.configure(image=self.master.dice[self.game_obj.player_two_roll_two - 1])

            self.player_one_calc_result = ""

            if self.game_obj.player_two_roll_one == self.game_obj.player_two_roll_two:
                self.player_one_calc_result += "You rolled a double, so you get an additional roll.\n"
                self.player_one_roll_again = True

            if (self.game_obj.player_two_roll_one + self.game_obj.player_two_roll_two) % 2 == 0:
                self.player_one_calc_result += "You rolled an even number.\nYour roll gains 10 points."
                self.player_one_round_score += 10

            else:
                self.player_one_calc_result += "You rolled an odd number.\nYour roll loses 5 points."
                self.player_one_round_score -= 5

            if self.player_one_round_score < 0:
                self.player_one_round_score = 0

            self.game_obj.player_two_score += self.player_one_round_score
            self.player_one_calc_box.configure(text=str(self.player_one_calc_result))
            self.player_one_round_score = 0

            if not self.player_one_roll_again:
                self.player_one_roll_button["state"] = "disabled"
                self.game_obj.player_turn = int(not (self.game_obj.player_turn))
                self.game_obj.round_no += 1
                self.s.sendall(pickle.dumps(self.game_obj))


class GameOverFrameOnline(tk.Frame):
    """A class that shows the results of the online game"""
    def __init__(self, master, p1_score, p2, p2_score):
        self.master = master
        tk.Frame.__init__(self, self.master, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.master.colour[1])
        self.pack_propagate(0)

        master.unbind("<Key-Shift_L>")

        with open(HIGH_SCORES_FILE, 'r') as f:
            result = ""
            players_and_scores = f.read().split("\n")
            players_and_scores.pop(-1)
            players_and_scores = sorted(players_and_scores, key=lambda score: int(score.split(' ')[1]), reverse=True)

            if len(players_and_scores) >= 10:
                for x, i in enumerate(range(10)):
                    result += f"{x + 1}: {players_and_scores[i].split(' ')[0]}: {players_and_scores[i].split(' ')[1]}\n"
            else:
                result_text = "Sorry, there are not enough scores to show."

        if p1_score > p2_score:
            result_text = f"Congratulations you won. The final score was: {p1_score}:{p2_score}"
        else:
            result_text = f"Unlucky, you lost. The final score was: {p1_score}:{p2_score}"

        self.results = tk.Label(self,
                                text=f"{result_text}\n\nYou can see the top 10 high scores below:",
                                bg=self.master.colour[1], fg=self.master.font_colour).pack(pady=40)

        self.high_scores_label = tk.Label(self, text=f"{result}", bg=self.master.colour[1],
                                          fg=self.master.font_colour).pack(pady=20)

        self.main_menu_button = tk.Button(self, text="Main Menu", bg=self.master.colour[1],
                                          highlightbackground=self.master.colour[1],
                                          command=lambda: master.switch_frame(GameMenu)).pack(pady=50)

        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=self.master.colour[1],
                                        fg=self.master.font_colour, font=(None, 10)).pack(side="bottom")
