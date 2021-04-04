import _thread
import pickle
import socket
import time
import tkinter as tk
from random import randint
from tkinter import messagebox
import pygame
from data.constants import *
import data.database as database
import data.security as security
from data.game_classes import *


class PlayerOneLoginPage(tk.Frame):

    def __init__(self, parent):
        self.parent = parent

        self.parent.title("Login")

        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])
        self.pack_propagate(0)
        self.alert_made = False

        self.login_label = tk.Label(self, text="Login", font=(FONT, TITLE_FONT_SIZE),
                                    fg=parent.font_colour, bg=parent.colour[1]).pack(pady=30)
        self.username_label = tk.Label(self, text="Username: ", bg=parent.colour[1], fg=parent.font_colour).pack(
            pady=10)
        self.username_entry = tk.Entry(self, bg=parent.colour[1], fg=parent.font_colour, borderwidth=1, relief="flat")
        self.username_entry.pack(pady=10)
        self.password_label = tk.Label(self, text="Password:", bg=parent.colour[1], fg=parent.font_colour).pack(pady=10)
        self.password_entry = tk.Entry(self, bg=parent.colour[1], show="*", fg=parent.font_colour, borderwidth=1,
                                       relief="flat")
        self.password_entry.pack(pady=10)
        self.login_button = tk.Button(self, text="Confirm", bg=parent.colour[1], highlightbackground=parent.colour[1],
                                      command=lambda: self.check_login(self.username_entry.get(),
                                                                       self.password_entry.get())).pack(pady=20)
        self.create_account_label = tk.Label(self, text="Don't have an account?\n\nCreate an account:",
                                             bg=parent.colour[1], fg=parent.font_colour).pack(pady=30)
        self.create_account_button = tk.Button(self, text="Confirm", bg=parent.colour[1],
                                               highlightbackground=parent.colour[1],
                                               command=lambda: self.parent.switch_frame(PlayerOneCreateAccountPage)
                                               ).pack(pady=10)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def check_login(self, username, password):

        global player_one

        if database.check_user(username, password):
            player_one = Player(username, password)
            colour = database.get_user_details(player_one.username)[2]
            volume = database.get_user_details(player_one.username)[3]

            self.parent.colour = self.parent.colours_dict[f"{colour}"][0]
            self.parent.font_colour = self.parent.colours_dict[f"{colour}"][1]
            self.parent.dice = self.parent.colours_dict[f"{colour}"][2]
            self.parent.configure(bg=self.parent.colours_dict[f"{colour}"][0][0])
            pygame.mixer.music.set_volume(float(volume))
            self.parent.switch_frame(GameMenu)

        elif not self.alert_made:
            alert_label = tk.Label(self,
                                   text="Sorry, the username or password you entered was incorrect."
                                        "\nPlease try again.",
                                   fg="orange", bg=self.parent.colour[1]).pack()
            self.alert_made = True


class PlayerOneCreateAccountPage(tk.Frame):

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])

        self.pack_propagate(0)

        self.alert_made = False

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: self.parent.switch_frame(PlayerOneLoginPage)).pack(anchor="nw",
                                                                                                        padx=5, pady=5)
        self.create_account_label = tk.Label(self, text="Create Account", font=(FONT, TITLE_FONT_SIZE),
                                             bg=self.parent.colour[1], fg=self.parent.font_colour).pack()
        self.username_label = tk.Label(self, text="New Username: ", bg=self.parent.colour[1],
                                       fg=self.parent.font_colour).pack(pady=20)
        self.username_entry = tk.Entry(self, bg=self.parent.colour[1], fg=self.parent.font_colour, borderwidth=1,
                                       relief="flat")
        self.username_entry.pack(pady=20)
        self.password_label = tk.Label(self, text="New Password: ", bg=self.parent.colour[1],
                                       fg=self.parent.font_colour).pack(pady=20)
        self.password_entry = tk.Entry(self, bg=self.parent.colour[1], show="*",
                                       fg=self.parent.font_colour, borderwidth=1, relief="flat")
        self.password_entry.pack(pady=20)
        self.confirm_password_label = tk.Label(self, text="Confirm New Password: ", bg=self.parent.colour[1],
                                               fg=self.parent.font_colour).pack(pady=20)
        self.confirm_password_entry = tk.Entry(self, bg=self.parent.colour[1], show="*",
                                               fg=self.parent.font_colour, borderwidth=1, relief="flat")
        self.confirm_password_entry.pack(pady=20)
        self.confirm_create_account_button = tk.Button(self, text="Confirm", bg=self.parent.colour[1],
                                                       highlightbackground=self.parent.colour[1],
                                                       command=lambda: self.confirm_new_account(
                                                           self.username_entry.get(), self.password_entry.get(),
                                                           self.confirm_password_entry.get())).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def confirm_new_account(self, username, password, confirm_password):
        global player_one

        valid = True if 2 < len(username) < 15 and 2 < len(password) < 15 else False

        if not database.does_user_exist(username) and password == confirm_password and valid:
            database.add_user(username, password, 'blue', 0.2)
            player_one = Player(username, password)
            self.parent.switch_frame(GameMenu)

        elif not self.alert_made:
            alert_label = tk.Label(self,
                                   text="Sorry, the username or password you entered was incorrect."
                                        "\nPlease try again.",
                                   fg="orange", bg=self.parent.colour[1]).pack()
            self.alert_made = True


class GameMenu(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])
        self.pack_propagate(0)

        parent.title(f"game Menu - {player_one.username}")

        self.game_menu_label = tk.Label(self, text="Game Menu", font=(FONT, TITLE_FONT_SIZE),
                                        fg=self.parent.font_colour, bg=self.parent.colour[1]).pack(pady=60)
        self.play_duo_button = tk.Button(self, text="Duo game", bg=self.parent.colour[1],
                                         highlightbackground=self.parent.colour[1], width=25, height=2,
                                         command=lambda: self.parent.switch_frame(PlayerTwoLoginPage)).pack(pady=20)
        self.play_online_button = tk.Button(self, text="Online game", bg=self.parent.colour[1],
                                            highlightbackgroun=self.parent.colour[1], width=25,
                                            height=2,
                                            command=lambda: self.parent.switch_frame(OnlineGameInitPage)).pack(
            pady=20)
        self.rules_button = tk.Button(self, text="Rules", bg=self.parent.colour[1],
                                      highlightbackground=self.parent.colour[1], width=25, height=2,
                                      command=lambda: self.parent.switch_frame(Rules)).pack(pady=20)
        self.settings_button = tk.Button(self, text="Settings", bg=self.parent.colour[1],
                                         highlightbackground=self.parent.colour[1], width=25, height=2,
                                         command=lambda: self.parent.switch_frame(Settings)).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")


class Settings(tk.Frame):

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])
        self.pack_propagate(0)

        parent.title(f"Settings - {player_one.username}")

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: self.parent.switch_frame(GameMenu))
        self.back_button.pack(anchor="nw",
                              padx=5, pady=5)
        self.game_menu_label = tk.Label(self, text="Settings", font=(FONT, TITLE_FONT_SIZE),
                                        fg=self.parent.font_colour, bg=self.parent.colour[1]).pack(pady=30)
        self.music_title_label = tk.Label(self, text="Music", font=(FONT, 25, "underline"), fg=self.parent.font_colour,
                                          bg=self.parent.colour[1]).pack(pady=10)
        self.music_volume_label = tk.Label(self, text="music Volume: ", fg=self.parent.font_colour,
                                           bg=self.parent.colour[1]).pack(pady=10)
        self.music_volume_scale = tk.Scale(self, orient="horizontal", bg=self.parent.colour[1], fg=parent.font_colour,
                                           length=80, troughcolor=self.parent.colour[1], showvalue=0,
                                           highlightcolor=self.parent.colour[1],
                                           highlightbackground=self.parent.colour[1],
                                           activebackground=self.parent.colour[1], command=self.change_volume)
        self.music_volume_scale.set(pygame.mixer.music.get_volume() * 100)
        self.music_volume_scale.pack(pady=10)
        self.themes_title_label = tk.Label(self, text="Themes", font=(FONT, 25, "underline"),
                                           fg=self.parent.font_colour, bg=self.parent.colour[1]).pack(pady=10)
        self.blue_theme_checkbox = tk.Checkbutton(self, text="Blue", bg=self.parent.colour[1],
                                                  fg=self.parent.font_colour)
        self.blue_theme_checkbox.pack(pady=10)
        self.green_theme_checkbox = tk.Checkbutton(self, text="Green", bg=self.parent.colour[1],
                                                   fg=self.parent.font_colour)
        self.green_theme_checkbox.pack(pady=10)
        self.black_theme_checkbox = tk.Checkbutton(self, text="Dark", bg=self.parent.colour[1],
                                                   fg=self.parent.font_colour)
        self.black_theme_checkbox.pack(pady=10)

        self.white_theme_checkbox = tk.Checkbutton(self, text="Light", bg=self.parent.colour[1],
                                                   fg=self.parent.font_colour)
        self.white_theme_checkbox.pack(pady=10)

        self.blue_theme_checkbox.configure(command=lambda: self.change_theme("blue", self.blue_theme_checkbox))
        self.green_theme_checkbox.configure(command=lambda: self.change_theme("green", self.green_theme_checkbox))
        self.black_theme_checkbox.configure(command=lambda: self.change_theme("black", self.black_theme_checkbox))
        self.white_theme_checkbox.configure(command=lambda: self.change_theme("white", self.white_theme_checkbox))

        self.log_out_button = tk.Button(self, text="Log Out", bg=self.parent.colour[1],
                                        highlightbackground=self.parent.colour[1],
                                        command=lambda: self.log_out())
        self.log_out_button.pack(anchor="se", padx=5)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")

        self.blue_theme_checkbox.deselect()
        self.green_theme_checkbox.deselect()
        self.black_theme_checkbox.deselect()
        self.white_theme_checkbox.deselect()

        if self.parent.colour == BLUE:
            self.blue_theme_checkbox.select()
        elif self.parent.colour == GREEN:
            self.green_theme_checkbox.select()
        elif self.parent.colour == BLACK:
            self.black_theme_checkbox.select()
        elif self.parent.colour == WHITE:
            self.white_theme_checkbox.select()

    def change_theme(self, theme, button):
        self.blue_theme_checkbox.deselect()
        self.green_theme_checkbox.deselect()
        self.black_theme_checkbox.deselect()
        self.white_theme_checkbox.deselect()
        button.select()

        if self.parent.colour == BLUE:
            current_colour = "blue"
        elif self.parent.colour == GREEN:
            current_colour = "green"
        elif self.parent.colour == BLACK:
            current_colour = "black"
        elif self.parent.colour == WHITE:
            current_colour = "white"

        database.update_user_theme(player_one.username, theme)


        self.parent.colour = self.parent.colours_dict[f"{theme}"][0]
        self.parent.font_colour = self.parent.colours_dict[f"{theme}"][1]
        self.parent.dice = self.parent.colours_dict[f"{theme}"][2]
        self.parent.configure(bg=self.parent.colours_dict[f"{theme}"][0][0])
        self.configure(bg=self.parent.colour[1])

        for i in self.pack_slaves():
            i.configure(bg=self.parent.colour[1], highlightbackground=self.parent.colour[1], fg=self.parent.font_colour)

        self.music_volume_scale.configure(troughcolor=self.parent.colour[1], activebackground=self.parent.colour[1])
        self.back_button.configure(fg="black")
        self.log_out_button.configure(fg="black")

    def change_volume(self, volume):
        database.update_user_volume(player_one.username, float(int(volume) / 100))

        pygame.mixer.music.set_volume(float(int(volume) / 100))

    def log_out(self):

        self.log_out_messagebox = messagebox.askokcancel(title='Confirm',
                                                         message='Are you sure you want to log out?')
        if self.log_out_messagebox:
            player_one.username = ""
            player_one.password = ""
            self.parent.colour = BLUE
            self.parent.font_colour = "white"
            self.parent.colours_dict = {"blue": [BLUE, "white", BLUE_DICE], "green": [GREEN, "white", GREEN_DICE],
                                        "black": [BLACK, "white", BLACK_DICE],
                                        "white": [WHITE, "black", WHITE_DICE]}

            self.parent.dice = BLUE_DICE
            self.configure(bg=self.parent.colour[1])
            self.parent.configure(bg=self.parent.colour[0])
            pygame.mixer.music.set_volume(0.2)

            self.parent.switch_frame(PlayerOneLoginPage)


class Rules(tk.Frame):

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])
        self.pack_propagate(0)

        self.parent.title(f"Rules - {player_one.username}")

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: parent.switch_frame(GameMenu)).pack(anchor="nw", padx=5, pady=5)

        self.rules_title_label = tk.Label(self, text="Rules", font=(FONT, 30),
                                          fg=self.parent.font_colour, bg=self.parent.colour[1]).pack(pady=40)

        self.rules_label = tk.Label(self,
                                    text='- In the dice game there are two dice, one belonging to each player.\n\n- Each player takes turns to roll their dice, once you receive a roll,\n\ndifferent points will be added and subtracted depending on its nature.\n\n- If a player rolls an even number, 10 points are added to their score.\n\n- If a player rolls an odd number, then 5 points are subtracted from their score,\n\nunless it would cause their score to become negative.\n\n- If a player rolls a double, they receive an additional roll.\n\n- There are five rounds, where each rounds of each player rolling their dice once.\n\n- If both players scores are the same at the end of the five rounds,\n\nthen additional rounds will commence until the scores are no longer the same. ',
                                    bg=self.parent.colour[1], fg=self.parent.font_colour).pack(pady=10)

        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=self.parent.colour[1],
                                        fg=self.parent.font_colour, font=(None, 10)).pack(side="bottom")


class PlayerTwoLoginPage(tk.Frame):

    def __init__(self, parent):
        self.parent = parent

        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])

        parent.title(f"Player Two Login - {player_one.username}")

        self.pack_propagate(0)
        self.alert_made = False

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: self.parent.switch_frame(GameMenu)).pack(anchor="nw",
                                                                                              padx=5, pady=5)
        self.player_two_login_label = tk.Label(self, text="Player Two Login", font=(FONT, TITLE_FONT_SIZE),
                                               fg=parent.font_colour, bg=parent.colour[1]).pack(pady=5)
        self.info_label = tk.Label(self, text="Information: you will be logged out\n at the end of the game.",
                                   bg=parent.colour[1], fg=parent.font_colour).pack(pady=5)
        self.username_label = tk.Label(self, text="Username: ", bg=parent.colour[1], fg=parent.font_colour).pack(
            pady=10)
        self.username_entry = tk.Entry(self, bg=parent.colour[1], fg=parent.font_colour, borderwidth=1, relief="flat")
        self.username_entry.pack(pady=10)
        self.password_label = tk.Label(self, text="Password:", bg=parent.colour[1], fg=parent.font_colour).pack(pady=5)
        self.password_entry = tk.Entry(self, bg=parent.colour[1], show="*", fg=parent.font_colour, borderwidth=1,
                                       relief="flat")
        self.password_entry.pack(pady=10)
        self.login_button = tk.Button(self, text="Confirm", bg=parent.colour[1], highlightbackground=parent.colour[1],
                                      command=lambda: self.check_login(self.username_entry.get(),
                                                                       self.password_entry.get())).pack(pady=20)
        self.create_account_label = tk.Label(self, text="Don't have an account?\n\nCreate an account:",
                                             bg=parent.colour[1], fg=parent.font_colour).pack(pady=10)
        self.create_account_button = tk.Button(self, text="Confirm", bg=parent.colour[1],
                                               highlightbackground=parent.colour[1],
                                               command=lambda: self.parent.switch_frame(PlayerTwoCreateAccountPage)
                                               ).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def check_login(self, username, password):
        global player_two

        if database.check_user(username, password):
            player_two = Player(username, password)
            self.parent.switch_frame(DuoGame)

        elif not self.alert_made:
            alert_label = tk.Label(self,
                                   text="Sorry, the username or password you entered was incorrect."
                                        "\nPlease try again.",
                                   fg="orange", bg=self.parent.colour[1]).pack()
            self.alert_made = True


class PlayerTwoCreateAccountPage(tk.Frame):
    "A class that allows player two to optionally create a page, if they cannot don't wont to login"

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])

        self.pack_propagate(0)
        parent.title(f"Player Two Create Account - {player_one.username}")

        self.alert_made = False

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: self.parent.switch_frame(PlayerTwoLoginPage)).pack(anchor="nw",
                                                                                                        padx=5, pady=5)
        self.create_account_label = tk.Label(self, text="Create Account", font=(FONT, TITLE_FONT_SIZE),
                                             bg=self.parent.colour[1], fg=self.parent.font_colour).pack()
        self.info_label = tk.Label(self, text="Information: you will be logged out\n at the end of the game.",
                                   bg=parent.colour[1], fg=parent.font_colour).pack(pady=15)
        self.username_label = tk.Label(self, text="New Username: ", bg=self.parent.colour[1],
                                       fg=self.parent.font_colour).pack(pady=10)
        self.username_entry = tk.Entry(self, bg=self.parent.colour[1], fg=self.parent.font_colour, borderwidth=1,
                                       relief="flat")
        self.username_entry.pack(pady=10)
        self.password_label = tk.Label(self, text="New Password: ", bg=self.parent.colour[1],
                                       fg=self.parent.font_colour).pack(pady=10)
        self.password_entry = tk.Entry(self, bg=self.parent.colour[1], show="*",
                                       fg=self.parent.font_colour, borderwidth=1, relief="flat")
        self.password_entry.pack(pady=10)
        self.confirm_password_label = tk.Label(self, text="Confirm New Password: ", bg=self.parent.colour[1],
                                               fg=self.parent.font_colour).pack(pady=10)
        self.confirm_password_entry = tk.Entry(self, bg=self.parent.colour[1], show="*",
                                               fg=self.parent.font_colour, borderwidth=1, relief="flat")
        self.confirm_password_entry.pack(pady=10)
        self.confirm_create_account_button = tk.Button(self, text="Confirm", bg=self.parent.colour[1],
                                                       highlightbackground=self.parent.colour[1],
                                                       command=lambda: self.confirm_new_account(
                                                           self.username_entry.get(), self.password_entry.get(),
                                                           self.confirm_password_entry.get())).pack(pady=30)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")

    def confirm_new_account(self, username, password, confirm_password):

        global player_two

        valid = True if 2 < len(username) < 15 and 2 < len(password) < 15 else False

        if not database.does_user_exist(username) and password == confirm_password and valid:
            player_two = Player(username, password)
            self.parent.switch_frame(DuoGame)


        elif not self.alert_made:
            alert_label = tk.Label(self,
                                   text="Sorry, the username or password you entered was incorrect."
                                        "\nPlease try again.",
                                   fg="orange", bg=self.parent.colour[1]).pack()
            self.alert_made = True


class DuoGame(tk.Frame):
    "A class that creates an instance of the duo game"

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[0])
        self.pack_propagate(0)

        parent.title(f"Duo game - {player_one.username} vs {player_two.username}")

        self.game = Game()

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[0],
                                     highlightbackground=self.parent.colour[0], command=lambda: self.quit_game()).pack(
            anchor="nw", padx=5, pady=5)

        self.title = tk.Label(self, text="Duo game", bg=self.parent.colour[0], fg=self.parent.font_colour,
                              font=(FONT, 30))
        self.title.grid(column=0, row=0, columnspan=3, pady=4)

        self.player_one_title = tk.Label(self, text="Player One: \n " + player_one.username, bg=self.parent.colour[0],
                                         fg=self.parent.font_colour,
                                         width=10)
        self.player_one_title.grid(column=0, row=1, sticky="N")

        self.player_score_title = tk.Label(self, text="Round: " + str(self.game.round) + "\n\nScore:\n" + str(
            player_one.score) + " : " + str(player_two.score),
                                           bg=self.parent.colour[0], fg=self.parent.font_colour, width=10)
        self.player_score_title.grid(column=1, row=1, sticky="N")

        self.player_two_title = tk.Label(self, text="Player Two: \n" + player_two.username, bg=self.parent.colour[0],
                                         fg=self.parent.font_colour,
                                         width=10)
        self.player_two_title.grid(column=2, row=1, sticky="N")

        self.player_one_frame = tk.Frame(self, bg=self.parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_one_frame.grid(column=0, row=2, sticky="N", padx=5)

        self.player_one_frame.pack_propagate(0)

        self.border_frame = tk.Frame(self, bg=self.parent.colour[0], width=WINDOW_WIDTH / 100 * 2)
        self.border_frame.grid(column=1, row=2)

        self.player_two_frame = tk.Frame(self, bg=self.parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_two_frame.grid(column=2, row=2, sticky="N", padx=5)

        self.player_two_frame.pack_propagate(0)

        self.player_one_dice_image_one = tk.Label(self.player_one_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_one_dice_image_one.pack(pady=5, side="top")

        self.player_one_dice_image_two = tk.Label(self.player_one_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_one_dice_image_two.pack(pady=5, side="top")

        self.player_one_calc_box = tk.Label(self.player_one_frame, text="Result:\nNothing", bg=self.parent.colour[1],
                                            fg=self.parent.font_colour,
                                            width=50, height=5)
        self.player_one_calc_box.pack(pady=10)

        self.player_two_dice_image_one = tk.Label(self.player_two_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_two_dice_image_one.pack(pady=5, side="top")

        self.player_two_dice_image_two = tk.Label(self.player_two_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_two_dice_image_two.pack(pady=5, side="top")

        self.player_two_calc_box = tk.Label(self.player_two_frame, text="Result:\nNothing", bg=self.parent.colour[1],
                                            fg=self.parent.font_colour,
                                            width=50, height=5)
        self.player_two_calc_box.pack(pady=10)

        self.player_one_roll_button = tk.Button(self.player_one_frame, text="ROLL!", bg=self.parent.colour[1],
                                                highlightbackground=self.parent.colour[1],
                                                command=lambda: self.roll(player_one, 1))
        self.player_one_roll_button.pack()

        self.player_one_info = tk.Label(self.player_one_frame, text="OR Press Left Shift!", bg=self.parent.colour[1],
                                        fg=self.parent.font_colour,
                                        height=5).pack(pady=10)

        self.player_two_roll_button = tk.Button(self.player_two_frame, text="ROLL!", bg=self.parent.colour[1],
                                                highlightbackground=self.parent.colour[1],
                                                command=lambda: self.roll(player_two, 2))
        self.player_two_roll_button.pack()

        self.player_two_tip = tk.Label(self.player_two_frame, text="OR Press Return!", bg=self.parent.colour[1],
                                       fg=self.parent.font_colour,
                                       height=5).pack(pady=10)

        self.player_two_roll_button["state"] = "disabled"

        self.parent.bind("<Key-Shift_L>", lambda event: self.roll(player_one, 1))
        self.parent.bind("<Key-Return>", lambda event: self.roll(player_two, 2))

    def roll(self, player, player_num):

        if self.game.round <= 5 or player_one.score == player_two.score:
            if player_num == 1 and self.game.turn == 1:
                player.roll_1 = randint(1, 6)
                player.roll_2 = randint(1, 6)
                player.round_score = player.roll_1 + player.roll_2
                player.roll_again = False

                self.player_one_dice_image_one.configure(image=self.parent.dice[player.roll_1 - 1])
                self.player_one_dice_image_two.configure(image=self.parent.dice[player.roll_2 - 1])

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
                    self.game.turn = 2

                self.player_score_title.configure(
                    text="Round: " + str(self.game.round) + "\n\nScore\n" + str(player_one.score) + ":" + str(
                        player_two.score))

            elif player_num == 2 and self.game.turn == 2:
                player.roll_1 = randint(1, 6)
                player.roll_2 = randint(1, 6)
                player.round_score = player.roll_1 + player.roll_2
                player.roll_again = False

                self.player_two_dice_image_one.configure(image=self.parent.dice[player.roll_1 - 1])
                self.player_two_dice_image_two.configure(image=self.parent.dice[player.roll_2 - 1])

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
                    self.game.turn = 1

                self.player_score_title.configure(
                    text="Round: " + str(self.game.round) + "\n\nScore\n" + str(player_one.score) + ":" + str(
                        player_two.score))

        else:

            self.parent.switch_frame(GameOverFrame)

    def quit_game(self):

        self.quit_messagebox = messagebox.askokcancel(title='Confirm',
                                                      message='Are you sure you want to quit?\ngame progress will not be saved!')
        if self.quit_messagebox:
            self.parent.switch_frame(GameMenu)


class GameOverFrame(tk.Frame):

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])
        self.pack_propagate(0)

        parent.title(f"game Over")

        parent.unbind("<Key-Shift_L>")
        parent.unbind("<Key-Return>")

        database.add_highscore(player_one.username, player_one.score)
        database.add_highscore(player_two.username, player_two.score)

        result = '\n'.join(database.show_ten_highscores())

        winner = f"{player_one.username}" if player_one.score > player_two.score else f"{player_two.username}"

        self.results = tk.Label(self,
                                text="Congratulations " + str(winner) + ", you won!\n\nThe final score was: " + str(
                                    player_one.score) + "-" + str(
                                    player_two.score) + ".\n\nAll scores will be saved in a file, and you can see the top 10 high scores below:",
                                bg=self.parent.colour[1], fg=self.parent.font_colour).pack(pady=40)

        self.high_scores_label = tk.Label(self, text=f"{result}", bg=self.parent.colour[1],
                                          fg=self.parent.font_colour).pack(pady=20)

        self.main_menu_button = tk.Button(self, text="Main Menu", bg=self.parent.colour[1],
                                          highlightbackground=self.parent.colour[1],
                                          command=lambda: parent.switch_frame(GameMenu)).pack(pady=50)

        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=self.parent.colour[1],
                                        fg=self.parent.font_colour, font=(None, 10)).pack(side="bottom")


class OnlineGameInitPage(tk.Frame):
    "A class that creates a page that asks for the details required for the online game"

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])

        self.pack_propagate(0)

        self.parent.title(f"Online game - {player_one.username}")

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: parent.switch_frame(GameMenu)).pack(anchor="nw", padx=5, pady=5)
        self.online_game_title_label = tk.Label(self, text="Online game", font=(FONT, 30),
                                                fg=self.parent.font_colour, bg=self.parent.colour[1]).pack(pady=20)
        self.online_game_info_label = tk.Label(self,
                                               text="Hi, welcome to online game!\nOnline game is just like duo game,  except\nyou play against people over a network\ninstead of on a single machine.\nHave fun!",
                                               fg=self.parent.font_colour, bg=self.parent.colour[1]).pack(pady=20)
        self.server_ip_label = tk.Label(self, text="Server IP:\n\ne.g. 192.168.1.1", fg=self.parent.font_colour,
                                        bg=self.parent.colour[1]).pack(pady=20)
        self.server_ip_entry = tk.Entry(self, fg=self.parent.font_colour,
                                        bg=self.parent.colour[1])
        self.server_ip_entry.pack(pady=20)
        self.play_button = tk.Button(self, text="Play", fg="black", width=5, bg=self.parent.colour[1],
                                     highlightbackground=self.parent.colour[1],
                                     command=lambda: self.parent.switch_frame(OnlineGamePage,
                                                                              self.server_ip_entry.get())).pack(pady=20)
        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=parent.colour[1], fg=parent.font_colour,
                                        font=(None, 10)).pack(side="bottom")






class OnlineGamePage(tk.Frame):
    "A page that creates an instance of the online game"

    def __init__(self, parent, server_ip):
        self.parent = parent
        self.server_ip = server_ip
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[0])
        self.pack_propagate(0)

        parent.title(f"game Over")

        self.back_button = tk.Button(self, text="back", bg=self.parent.colour[0],
                                     highlightbackground=self.parent.colour[0],
                                     command=lambda: self.parent.switch_frame(GameMenu)).pack(
            anchor="nw", padx=5, pady=5)

        self.title = tk.Label(self, text="Online game", bg=self.parent.colour[0], fg=self.parent.font_colour,
                              font=(FONT, 30))
        self.title.grid(column=0, row=0, columnspan=3, pady=4)

        self.player_one_title = tk.Label(self, text="Player One: \n " + player_one.username, bg=self.parent.colour[0],
                                         fg=self.parent.font_colour,
                                         width=10)
        self.player_one_title.grid(column=0, row=1, sticky="N")

        self.player_score_title = tk.Label(self, text=f"Round: 0\n\nScore:\n0:0", bg=self.parent.colour[0],
                                           fg=self.parent.font_colour, width=10)
        self.player_score_title.grid(column=1, row=1, sticky="N")

        self.player_two_title = tk.Label(self, text="Player Two:\n Waiting...", bg=self.parent.colour[0],
                                         fg=self.parent.font_colour,
                                         width=20)
        self.player_two_title.grid(column=2, row=1, sticky="N")

        self.player_one_frame = tk.Frame(self, bg=self.parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_one_frame.grid(column=0, row=2, sticky="N", padx=5)

        self.player_one_frame.pack_propagate(0)

        self.border_frame = tk.Frame(self, bg=self.parent.colour[0], width=WINDOW_WIDTH / 100 * 2)
        self.border_frame.grid(column=1, row=2)

        self.player_two_frame = tk.Frame(self, bg=self.parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                                         height=WINDOW_HEIGHT / 4 * 3)
        self.player_two_frame.grid(column=2, row=2, sticky="N", padx=5)

        self.player_two_frame.pack_propagate(0)

        self.player_one_dice_image_one = tk.Label(self.player_one_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_one_dice_image_one.pack(pady=5, side="top")

        self.player_one_dice_image_two = tk.Label(self.player_one_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_one_dice_image_two.pack(pady=5, side="top")

        self.player_one_calc_box = tk.Label(self.player_one_frame, text="Result:\nNothing", bg=self.parent.colour[1],
                                            fg=self.parent.font_colour,
                                            width=50, height=5)
        self.player_one_calc_box.pack(pady=10)

        self.player_two_dice_image_one = tk.Label(self.player_two_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_two_dice_image_one.pack(pady=5, side="top")

        self.player_two_dice_image_two = tk.Label(self.player_two_frame, bg=self.parent.colour[1],
                                                  image=self.parent.dice[5])
        self.player_two_dice_image_two.pack(pady=5, side="top")

        self.player_two_calc_box = tk.Label(self.player_two_frame, text="Result:\nNothing", bg=self.parent.colour[1],
                                            fg=self.parent.font_colour,
                                            width=50, height=5)
        self.player_two_calc_box.pack(pady=10)

        self.player_one_roll_button = tk.Button(self.player_one_frame, text="ROLL!", bg=self.parent.colour[1],
                                                highlightbackground=self.parent.colour[1],
                                                command=lambda: self.roll(self.actual_player_no))
        self.player_one_roll_button.pack()
        self.player_one_roll_button['state'] = 'disabled'

        self.player_one_info = tk.Label(self.player_one_frame, text="OR Press Left Shift!", bg=self.parent.colour[1],
                                        fg=self.parent.font_colour,
                                        height=5).pack(pady=10)

        self.parent.bind("<Key-Shift_L>", lambda event: self.roll(self.actual_player_no))

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
                                        image=self.parent.dice[self.game_obj.player_two_roll_one - 1])
                                    self.player_two_dice_image_two.configure(
                                        image=self.parent.dice[self.game_obj.player_two_roll_two - 1])

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
                                        image=self.parent.dice[self.game_obj.player_one_roll_one - 1])
                                    self.player_two_dice_image_two.configure(
                                        image=self.parent.dice[self.game_obj.player_one_roll_two - 1])

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
                                    self.parent.switch_frame(GameOverFrameOnline, self.game_obj.player_one_score,
                                                             self.game_obj.player_two_name,
                                                             self.game_obj.player_two_score)
                                elif self.actual_player_no == 1:
                                    self.parent.switch_frame(GameOverFrameOnline, self.game_obj.player_two_score,
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
                    self.parent.switch_frame(OnlineGameInitPage)

    def roll(self, player):
        if player == 0 and self.game_obj.player_turn == 0:
            self.game_obj.player_one_roll_one = randint(1, 6)
            self.game_obj.player_one_roll_two = randint(1, 6)
            self.player_one_round_score = self.game_obj.player_one_roll_one + self.game_obj.player_one_roll_two
            self.player_one_roll_again = False

            self.player_one_dice_image_one.configure(image=self.parent.dice[self.game_obj.player_one_roll_one - 1])
            self.player_one_dice_image_two.configure(image=self.parent.dice[self.game_obj.player_one_roll_two - 1])

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

            self.player_one_dice_image_one.configure(image=self.parent.dice[self.game_obj.player_two_roll_one - 1])
            self.player_one_dice_image_two.configure(image=self.parent.dice[self.game_obj.player_two_roll_two - 1])

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

    def __init__(self, parent, p1_score, p2, p2_score):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=self.parent.colour[1])
        self.pack_propagate(0)

        parent.unbind("<Key-Shift_L>")


        result = '\n'.join(database.show_ten_highscores())


        if p1_score > p2_score:
            result_text = f"Congratulations you won. The final score was: {p1_score}:{p2_score}"
        else:
            result_text = f"Unlucky, you lost. The final score was: {p1_score}:{p2_score}"

        self.results = tk.Label(self,
                                text=f"{result_text}\n\nYou can see the top 10 high scores below:",
                                bg=self.parent.colour[1], fg=self.parent.font_colour).pack(pady=40)

        self.high_scores_label = tk.Label(self, text=f"{result}", bg=self.parent.colour[1],
                                          fg=self.parent.font_colour).pack(pady=20)

        self.main_menu_button = tk.Button(self, text="Main Menu", bg=self.parent.colour[1],
                                          highlightbackground=self.parent.colour[1],
                                          command=lambda: parent.switch_frame(GameMenu)).pack(pady=50)

        self.watermark_label = tk.Label(self, text="© Toby Hogan 2020", bg=self.parent.colour[1],
                                        fg=self.parent.font_colour, font=(None, 10)).pack(side="bottom")
