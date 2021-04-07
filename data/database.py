import sqlite3
import data.security as security


def add_user(username, password, theme, volume):
    password = security.hash(password)

    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, theme, volume))

    conn.commit()
    conn.close()


# function to create a new user and add them to the database, used in the player one and two create account pages

def check_user(username, password):
    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    try:
        valid = True if security.check_hash(password, c.fetchone()[1]) else False
    except:
        valid = False

    conn.commit()
    conn.close()
    return valid


# function to check a user's credentials are correct, returns true if they are returns false if not

def update_user_volume(user, update_to):
    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("UPDATE users SET volume = ? WHERE username = ?", (update_to, user))

    conn.commit()
    conn.close()


# function to change the volume stored to a user account in the database when they change their volume in settings

def update_user_theme(user, update_to):
    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("UPDATE users SET theme = ? WHERE username = ?", (update_to, user))

    conn.commit()
    conn.close()


# function to chnage the theme stored to a user account in a database when they change their theme in settings

def does_user_exist(username):
    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    exists = False if c.fetchall() == [] else True

    conn.commit()
    conn.close()
    return exists


# function to see if a user exists already, to ensure when an account is made, a pre-existing usernames is not chosen, returns true or false

def get_user_details(username):
    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    details = c.fetchone()

    conn.commit()
    conn.close()
    return details


# function to return all information stored in the user_info database about a user, useful for changing theme and volume when they login


def reveal_users_table():
    conn = sqlite3.connect('data/user_info.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM users")
    print('____USERS TABLE____')
    for i in c.fetchall():
        print(i)

    conn.commit()
    conn.close()


# function to show the entire user_info database - useful for debugging

def add_highscore(username, highscore):
    conn = sqlite3.connect('data/high_scores.db')
    c = conn.cursor()

    c.execute("INSERT INTO scores VALUES (?, ?)", (username, highscore))

    conn.commit()
    conn.close()

# function to add a new score to the high_scores database, when a game finishes two are added


def show_ten_highscores():
    "returns 10 highscores ordered from highest to lowest as a list"
    conn = sqlite3.connect('data/high_scores.db')
    c = conn.cursor()

    c.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
    highscores = c.fetchall()
    highscores = [f'{i[0]}: {i[1]}' for i in highscores]

    conn.commit()
    conn.close()
    return highscores

# function to give the ten highest scores - used in the end screen after a game has finished


def reveal_scores_table():
    conn = sqlite3.connect('data/high_scores.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM scores")
    print('____HIGHSCORES TABLE____')
    for i in c.fetchall():
        print(i)

    conn.commit()
    conn.close()

# function to show the entire scores table - useful for debugging

# conn = sqlite3.connect("data/user_info.db")
# c = conn.cursor()
# c.execute("""CREATE TABLE users (
#         username text,
#         password text,
#         theme text,
#         volume integer
#     )""")

# c.execute("INSERT INTO users VALUES ('toby', 'password', 'blue', 0.2)")
# conn.close()

# function to add a user that can be executed from the terminal if needed

