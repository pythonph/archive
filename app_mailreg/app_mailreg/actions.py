from random import SystemRandom

from app_mailreg.models import *
from app_mailreg.util import ntoken_generate, password_encrypt, password_verify


def user_register(username, email, password, session):
    user = UserDB(username, hash=password_encrypt(password))
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
    notification = UserNotification(ntoken_generate, user.id_user, "verify")
    try:
        session.add(notification)
    except Exception:
        return False
    # Send email.
    return True


def user_verify(username, token):
    pass


def user_reset(username):
    pass
