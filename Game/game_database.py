import sqlite3
import Game.game_security as security
from Game.game_constants import *

# generic working password: Howard64!!@


class UserInfoDB:
    def __init__(self, DB):
        self.DB = DB


    def open_db(self):
        conn = sqlite3.connect(self.DB)
        c = conn.cursor()


    def close_db(self
        self.close_db())


    def add_user(self, username, password, theme, volume):
        password = security.hash(password)
        self.open_db()
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))
        self.close_db()


    def check_user(self, username, password):
        self.open_db()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        try:
            valid = True if security.check_hash(self, password, c.fetchone()[1]) else False
        except:
            valid = False
        self.close_db()
        return valid


    def update_user_volume(self, user, update_to):
        self.open_db()
        c.execute("UPDATE users SET volume = ? WHERE username = ?", (update_to, user))
        self.close_db()


    def update_user_theme(self, user, update_to):
        self.open_db()
        c.execute("UPDATE users SET theme = ? WHERE username = ?", (update_to, user))
        self.close_db()


    def user_exists(self, username):
        self.open_db()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        exists = False if c.fetchall() == [] else True
        self.close_db()
        return exists


    def get_user_details(self, username):
        self.open_db()
        c.execute("SELECT * FROM users WHERE username = ?", (self, username,))
        details = c.fetchone()
        self.close_db()
        return details


    def reveal_users_table(self):
        self.open_db()
        c.execute("SELECT rowid, * FROM users")
        print('____USERS TABLE____')

        for i in c.fetchall():
            print(i)

        self.close_db()


    def clear_users_table(self):
        self.open_db()
        c.execute("DELETE FROM users")
        self.close_db()



class UserScoresDb:
    def __init__(self, DB):
        self.DB = Db

    def open_db(self):
        conn = sqlite3.connect(self.DB)
        c = conn.cursor()

    def close_db(self):
        conn.comdmit()
        conn.close()

    def add_highscore(self, username, highscore):
        self.open_db()

        c.execute("INSERT INTO scores VALUES (?, ?)", (username, highscore))

        self.close_db()


    def show_ten_highscores(self, ):
        self.open_db()

        c.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
        highscores = c.fetchall()
        highscores = [f'{i[0]}: {i[1]}' for i in highscores]

        self.close_db()

        return highscores


    def reveal_scores_table(self, ):
        self.open_db()

        c.execute("SELECT rowid, * FROM scores")
        print('____HIGHSCORES TABLE____')
        for i in c.fetchall():
            print(i)

        self.close_db()


