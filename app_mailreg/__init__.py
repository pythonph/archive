
__version__ = "0.0.1"


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


import app_mailreg.views
