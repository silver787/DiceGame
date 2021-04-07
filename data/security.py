import bcrypt
import re


# imports the regex and bcrypt modules - regex used to make advanced patterns for searching, bcrypt for encryption

def hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


# makes a hash from a password, also salts the password before hashing for added security


def check_hash(password, hash):
    return True if bcrypt.checkpw(password.encode('utf-8'), hash) else False


# compares a password to hashed and salted password to see if they are the same - used for user login


def password_check_hard(password):
    length_error = len(password) < 8

    digit_error = re.search(r"\d", password) is None

    uppercase_error = re.search(r"[A-Z]", password) is None

    lowercase_error = re.search(r"[a-z]", password) is None

    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return password_ok

# function to check a password meets strength criteria
