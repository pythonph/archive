import random
from base64 import urlsafe_b64encode

from Crypto.Random.random import StrongRandom
from Crypto.Util.number import long_to_bytes
from passlib.hash import bcrypt
from flask.ext.login import UserMixin

from app_mailreg import app, login_manager


__all__ = ["ntoken_generate", "password_encrypt", "password_verify"]


try:
    _ntoken_rng = random.SystemRandom()
except NotImplementedError:
    _ntoken_rng = StrongRandom()


def ntoken_generate():
    """
    Generates url-safe base-64 string for notification tokens.

    """

    rbits = _ntoken_rng.getrandbits(app.config["NTOKEN_RANDOM_BITS"])
    return urlsafe_b64encode(long_to_bytes(rbits))


def password_encrypt(password):
    return bcrypt.encrypt(password, rounds=app.config["BCRYPT_WORKFACTOR"])


def password_verify(password, hash):
    return bcrypt.verify(password, hash)


class User(UserMixin):

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.userdb.active

    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return self.id

    def authenticate(self):
        try:
            p = password_verify(self.password, self.userdb.hash)
            return p and self.userdb.is_active and self.userdb.is_verified
        except Exception:
            return False

    def __init__(self, id, password=None, userdb=None):
        self.id = unicode(id)
        self.userdb = userdb if userdb else UserDB.query.filter_by(name_user=self.id).first()
        self.anonymous = False if self.userdb else True
        self.password = password


@login_manager.user_loader
def load_user(id):
    u = UserDB.query.filter_by(name_user=id).first()
    return User(u.name_user, userdb=u) if u else None
