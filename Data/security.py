import bcrypt


def hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_hash(password, hash):
    return True if bcrypt.checkpw(password.encode('utf-8'), hash) else False





