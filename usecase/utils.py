import hashlib

mySalt = "$2b$12$6rMnsklapuHBKL."


def hash_password(password: str):
    pwd_hash = hashlib.sha256((password + mySalt).encode("utf-8"))
    return pwd_hash.hexdigest()
