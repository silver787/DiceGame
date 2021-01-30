import sqlite3
import Data.security as security


def add_user(username, password, theme, volume):
    password = security.hash(password)
    print(password)

    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))

    conn.commit()
    conn.close()


def check_user(username, password):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    return True if security.check_hash(password, c.fetchone()[1]) else False

    conn.commit()
    conn.close()


def update_user():
    pass
