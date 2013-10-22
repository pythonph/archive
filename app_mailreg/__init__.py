
__version__ = "0.0.1"


import time
import random
from hashlib import md5

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_object("app_mailreg.settings")
login_manager = LoginManager()
login_manager.setup_app(app)
db = SQLAlchemy(app)
csrf = CsrfProtect(app)


def ntokenrng_seed():
    """
    Seed provider for pseudo-random number generator for notification tokens

    """

    md = md5()
    md.update(str(time.time() * app.config["NTOKENRNG_SEEDSALT0"]))
    md.update(app.config["NTOKENRNG_SEEDSALT1"])
    return md.digest()

# TODO: Setup the random generator for notification tokens
try:
    rng_ntoken = random.SystemRandom()
except NotImplementedError:
    pass


import app_mailreg.views
