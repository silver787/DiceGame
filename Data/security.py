import bcrypt


def hash(password):
    return bcrypt.hashpw(password, gensalt())


def check_hash(password, hash):
    return True if bcrypt.checkpw(password, hash) else False
