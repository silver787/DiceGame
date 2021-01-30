import sqlite3
import Data.security


def add_user(username, password, theme, volume):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))


    conn.commit()
    conn.close()
