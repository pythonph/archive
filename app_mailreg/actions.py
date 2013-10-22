from random import SystemRandom

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
    contact = UserContact(user.id_user, user.name_user)
    try:
        session.add(contact)
    except Exception:
        return False
    contact_email = ContactEmail(contact.id_contact, email)
    try:
        session.add(contact_email)
    except Exception:
        return False

    #notification = UserNotification(user.id_user,s)


def user_verify(username, token):
    pass

def user_reset(username):
    pass
