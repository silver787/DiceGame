import bcrypt

password = b"SecretPassword55"

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

if bcrypt.checkpw(password, hashed):
    print("It matches")

else:
    print('no')