import sqlite3
import Data.security as security


def add_user(username, password, theme, volume):
    password = security.hash(password)

    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))

    conn.commit()
    conn.close()


def check_user(username, password):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    valid = True if security.check_hash(password, c.fetchone()[1]) else False

    conn.commit()
    conn.close()
    return valid


def update_user_volume(user, update_to):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("UPDATE users SET volume = ? WHERE username = ?", (update_to, user))

    conn.commit()
    conn.close()


def update_user_theme(user, update_to):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("UPDATE users SET theme = ? WHERE username = ?", (update_to, user))

    conn.commit()
    conn.close()


def does_user_exist(username):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    exists = False if c.fetchall() == [] else True

    conn.commit()
    conn.close()
    return exists


def get_user_details(username):
    conn = sqlite3.connect('Data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    details = c.fetchone()

    conn.commit()
    conn.close()
    return details


"""
conn = sqlite3.connect('Data/user_info.db')
c = conn.cursor()

c.execute("SELECT rowid, * FROM users")
print('____TABLE____')
for i in c.fetchall():
    print(i)

conn.commit()
conn.close()"""
