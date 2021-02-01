from Game.game_classes import *
from Game.game_constants import *
from Game.game_functions import *
import Game.game_security as security
import Game.game_database as database
import tkinter as tk
import pygame


class P1Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title("Login")
        self.alert_made = False

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
            p1 = Player(username)
            colour, volume = database.get_user_details(p1.username)[2:4]
            switch_user(self.parent, colour, volume)
            self.parent.switch_frame(GameMenu)

        elif not self.alert_made:
            self.alert = AlertLabel(self, self.parent, "Invalid credentials", 0, 10)
            self.alert_made = True


class P1Create(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title("Create Account")
        self.alert_made = False

        self.back_button = BackButton(self, self.parent, P1Login)
        self.title = TitleLabel(self, self.parent, 'Create Account', 0, 30)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.confirm_password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.confirm_password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_create_account = TextButton(self, self.parent, 'Confirm', lambda: self.create_account(), 0, 20)
        self.watermark = WatermarkLabel(self, self.parent)

    def create_account(self):
        global p1

        username, password = self.username_entry.get(), self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        pass_check_result = security.password_check(password, confirm_password)

        if pass_check_result is None:
            if not database.user_exists(username):
                p1 = Player(username)
                database.add_user(username, password, 'blue', 0.2)
                switch_user(self.parent, 'blue', 0.2)
                self.parent.switch_frame(GameMenu)

            elif not self.alert_made:
                self.alert = AlertLabel(self, self.parent, "Username already taken", 0, 10)
                self.alert_made = True

            elif self.alert_made:
                self.alert.destroy()
                self.alert = AlertLabel(self, self.parent, "Username already taken", 0, 10)

        elif not self.alert_made:
            self.alert = AlertLabel(self, self.parent, pass_check_result, 0, 10)
            self.alert_made = True

        elif self.alert_made:
            self.alert.destroy()
            self.alert = AlertLabel(self, self.parent, pass_check_result, 0, 10)


class GameMenu(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.alert_made = False
        self.parent.title(f"Game Menu - {p1.username}")

        self.title = TitleLabel(self, self.parent, 'Game Menu', 0, 60)
        self.duo_button = MenuButton(self, self.parent, "Duo Game",
                                     lambda: self.parent.switch_frame(DuoGame), 25, 2, 0, 20)
        self.online_button = MenuButton(self, self.parent, "Online Game",
                                        lambda: self.parent.switch_frame(OnlineGame), 25, 2, 0, 20)
        self.rules_button = MenuButton(self, self.parent, "Rules",
                                       lambda: self.parent.switch_frame(Rules), 25, 2, 0, 20)
        self.settings_button = MenuButton(self, self.parent, "Settings",
                                          lambda: self.parent.switch_frame(Settings), 25, 2, 0, 20)
        self.watermark = WatermarkLabel(self, self.parent)


class Settings(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title(f"Settings - {p1.username}")
        self.alert_made = False

        self.back_button = BackButton(self, self.parent, GameMenu)
        self.title = TitleLabel(self, self.parent, "Settings", 0, 30)
        self.music_subtitle = UnderlineSubtitle(self, self.parent, "Music", 0, 10)
        self.music_volume_label = TextLabel(self, self.parent, "Music Volume:", 0, 10)
        self.volume_scale = VolumeScale(self, self.parent, self.change_volume, 0, 10)
        self.themes_subtitle = UnderlineSubtitle(self, self.parent, "Themes", 0, 10)
        self.blue_checkbox = ThemeCheckbox(self, self.parent, 'Blue', 0, 10)
        self.green_checkbox = ThemeCheckbox(self, self.parent, 'Green', 0, 10)
        self.black_checkbox = ThemeCheckbox(self, self.parent, 'Black', 0, 10)
        self.white_checkbox = ThemeCheckbox(self, self.parent, 'White', 0, 10)
        self.log_out_button = tk.Button(self, text="Log Out", bg=self.parent.colour[1],
                                        highlightbackground=self.parent.colour[1],
                                        command=lambda: self.log_out())
        self.log_out_button.pack(anchor='se', padx=5)
        self.watermark = WatermarkLabel(self, self.parent)

        self.volume_scale.set(pygame.mixer.music.get_volume() * 100)
        if self.parent.colour == BLUE:
            self.blue_checkbox.select()
        elif self.parent.colour == GREEN:
            self.green_checkbox.select()
        elif self.parent.colour == BLACK:
            self.black_checkbox.select()
        elif self.parent.colour == WHITE:
            self.white_checkbox.select()


    def change_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)
        database.update_user_volume(p1.username, pygame.mixer.music.get_volume())

    def change_theme(self, theme, button):
        self.blue_checkbox.deselect()
        self.green_checkbox.deselect()
        self.black_checkbox.deselect()
        self.white_checkbox.deselect()
        button.select()

        database.update_user_theme(p1.username, theme)
        if theme == 'blue':
            self.parent.colour = BLUE
            self.parent.font_colour = 'white'
        elif theme == 'green':
            self.parent.colour = GREEN
            self.parent.font_colour = 'white'
        elif theme == 'black':
            self.parent.colour = BLACK
            self.parent.font_colour = 'white'
        elif theme == 'white':
            self.parent.colour = WHITE
            self.parent.font_colour = 'black'

        self.configure(bg=self.parent.colour[1])
        self.parent.configure(bg=self.parent.colour[0])
        self.volume_scale.configure(troughcolor=self.parent.colour[1], activebackground=self.parent.colour[1])

        for i in self.pack_slaves():
            i.configure(bg=self.parent.colour[1], highlightbackground=self.parent.colour[1], fg=self.master.font_colour)

        self.back_button.configure(fg='black')
        self.log_out_button.configure(fg='black')

    def log_out():
        pass





