import bcrypt
import re


def hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_hash(password, hash):
    return True if bcrypt.checkpw(password.encode('utf-8'), hash) else False


def password_check(password, confirm_password):
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
