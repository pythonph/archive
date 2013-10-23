import random
from base64 import urlsafe_b64encode

import Crypto.Random.random import StrongRandom
from Crypto.Util.number import long_to_bytes
from passlib.hash import bcrypt

from app_mailreg import app.config


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
