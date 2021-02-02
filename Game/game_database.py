import sqlite3
import Game.game_security as security
from Game.game_constants import *

# generic working password: Howard64!!@


def add_user(username, password, theme, volume):
    password = security.hash(password)

    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))

    conn.commit()
    conn.close()


def check_user(username, password):
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    try:
        valid = True if security.check_hash(password, c.fetchone()[1]) else False
    except:
        valid = False

    conn.commit()
    conn.close()

    return valid


def update_user_volume(user, update_to):
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("UPDATE users SET volume = ? WHERE username = ?", (update_to, user))

    conn.commit()
    conn.close()


def update_user_theme(user, update_to):
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("UPDATE users SET theme = ? WHERE username = ?", (update_to, user))

    conn.commit()
    conn.close()


def user_exists(username):
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    exists = False if c.fetchall() == [] else True

    conn.commit()
    conn.close()

    return exists


def get_user_details(username):
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    details = c.fetchone()

    conn.commit()
    conn.close()

    return details


def reveal_users_table():
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM users")
    print('____USERS TABLE____')
    for i in c.fetchall():
        print(i)

    conn.commit()
    conn.close()


def clear_users_table():
    conn = sqlite3.connect(USER_INFO_DB)
    c = conn.cursor()

    c.execute("DELETE FROM users")

    conn.commit()
    conn.close()



def add_highscore(username, highscore):
    conn = sqlite3.connect(HIGH_SCORES_DB)
    c = conn.cursor()

    c.execute("INSERT INTO scores VALUES (?, ?)", (username, highscore))

    conn.commit()
    conn.close()


def show_ten_highscores():
    conn = sqlite3.connect(HIGH_SCORES_DB)
    c = conn.cursor()

    c.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
    highscores = c.fetchall()
    highscores = [f'{i[0]}: {i[1]}' for i in highscores]

    conn.commit()
    conn.close()
    return highscores


def reveal_scores_table():
    conn = sqlite3.connect(HIGH_SCORES_DB)
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM scores")
    print('____HIGHSCORES TABLE____')
    for i in c.fetchall():
        print(i)

    conn.commit()
    conn.close()


def add_game(game_code, p1, p1_score, turn, p2, p2_score, round):
    conn = sqlite3.connect(SAVED_GAMES_DB)
    c = conn.cursor()

    c.execute("INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?, ?)", (game_code, p1, p1_score, turn, p2, p2_score, round))

    conn.commit()
    conn.close()


def does_game_code_exist(code):
    conn = sqlite3.connect(SAVED_GAMES_DB)
    c = conn.cursor()

    c.execute("SELECT * FROM games WHERE code = ?", (code,))
    exists = False if c.fetchall() == [] else True

    conn.commit()
    conn.close()

    return exists


def reveal_games_table():
    conn = sqlite3.connect(SAVED_GAMES_DB)
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM scores")
    print('____HIGHSCORES TABLE____')
    for i in c.fetchall():
        print(i)

    conn.commit()
    conn.close()


def clear_games_table():
    conn = sqlite3.connect(SAVED_GAMES_DB)
    c = conn.cursor()

    c.execute("DELETE FROM users")

    conn.commit()
    conn.close()

