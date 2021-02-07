from game.game_constants import *
import bcrypt
import pygame
import random
import random
import re
import sqlite3
import string
import tkinter as tk


class UserDB:
    def __init__(self, security):
        self.security = security

    def add_user(self, username, password, theme, volume):
        password = self.security.hash(password)

        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))

        conn.commit()
        conn.close()

    def check_user(self, username, password):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        try:
            valid = True if self.security.check_hash(password, c.fetchone()[1]) else False
        except Exception as e:
            valid = False

        conn.commit()
        conn.close()

        return valid

    def update_user_volume(self, user, update_to):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("UPDATE users SET volume = ? WHERE username = ?", (update_to, user))

        conn.commit()
        conn.close()

    def update_user_theme(self, user, update_to):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("UPDATE users SET theme = ? WHERE username = ?", (update_to, user))

        conn.commit()
        conn.close()

    def user_exists(self, username):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        exists = False if c.fetchall() == [] else True

        conn.commit()
        conn.close()

        return exists

    def get_user_details(self, username):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        details = c.fetchone()

        conn.commit()
        conn.close()

        return details

    def reveal_users_table(self):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM users")
        print('____USERS TABLE____')
        for i in c.fetchall():
            print(i)

        conn.commit()
        conn.close()

    def clear_users_table(self):
        conn = sqlite3.connect(USER_INFO_DB)
        c = conn.cursor()

        c.execute("DELETE FROM users")

        conn.commit()
        conn.close()


class HighscoresDB:
    def add_highscore(self, username, highscore):
        conn = sqlite3.connect(HIGH_SCORES_DB)
        c = conn.cursor()

        c.execute("INSERT INTO scores VALUES (?, ?)", (username, highscore))

        conn.commit()
        conn.close()

    def twenty_scores(self):
        conn = sqlite3.connect(HIGH_SCORES_DB)
        c = conn.cursor()

        c.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 2 0")
        highscores = c.fetchall()
        highscores = [f'{i[0]}: {i[1]}' for i in highscores]

        conn.commit()
        conn.close()
        return highscores

    def reveal_scores_table(self):
        conn = sqlite3.connect(HIGH_SCORES_DB)
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM scores")
        print('____HIGHSCORES TABLE____')
        for i in c.fetchall():
            print(i)

        conn.commit()
        conn.close()


class Security:
    def hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_hash(self, password, hash):
        return True if bcrypt.checkpw(password.encode('utf-8'), hash) else False

    def password_check(self, password, confirm_password):
        if len(password) < 8:
            return "Password too short"

        if re.search(r"\d", password) is None:
            return "Password does not contain numbers"

        if re.search(r"[A-Z]", password) is None:
            return "Password has no upppercase characters"

        if re.search(r"[a-z]", password) is None:
            return "Password does not contain lowercase characters"

        if re.search(r"\W", password) is None:
            return "Password does not contain any symbols"

        if password != confirm_password:
            return "Passwords do not match"


class Helper:
    def switch_user(self, parent, colour, volume):
        if colour == 'blue':
            parent.colour = BLUE
            parent.font_colour = 'white'
            parent.dice = BLUE_DICE
            parent.configure(bg=parent.colour[0])
            pygame.mixer.music.set_volume(volume)

        elif colour == 'green':
            parent.colour = GREEN
            parent.font_colour = 'white'
            parent.dice = GREEN_DICE
            parent.configure(bg=parent.colour[0])
            pygame.mixer.music.set_volume(volume)

        elif colour == 'black':
            parent.colour = BLACK
            parent.font_colour = 'white'
            parent.dice = BLACK_DICE
            parent.configure(bg=parent.colour[0])
            pygame.mixer.music.set_volume(volume)

        elif colour == 'white':
            parent.colour = WHITE
            parent.font_colour = 'white'
            parent.dice = WHITE_DICE
            parent.configure(bg=parent.colour[0])
            pygame.mixer.music.set_volume(volume)


class Player:
    def __init__(self, username, num):
        self.username = username
        self.score = 0
        self.roll_1 = 0
        self.roll_2 = 0
        self.num = num
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
        self.turn = 1
