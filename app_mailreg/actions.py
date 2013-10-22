from passlib.hash import bcrypt

from app_mailreg import app
from app_mailreg.models import *

def user_register(username, email, password, session):
    hash = bcrypt.encrypt(password, rounds=app.config["BCRYPT_WORKFACTOR"])
    user = UserDB(username, hash=hash)
    try:
        session.add(user)
    except Exception:
        # TODO: Catch db errors - existing usernames
        return False


def user_verify(username, token):
    pass

def user_reset(username):
    pass
