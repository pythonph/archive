import os.path as path
from datetime import datetime, date, timedelta


from flask import (
    render_template, Response, request, session, redirect, url_for, flash,
    send_from_directory, g)
from flask.ext.login import (
    current_user, login_user, logout_user, login_required, UserMixin)
from passlib.hash import bcrypt


from app_mailreg import app, login_manager, db
from app_mailreg.forms import *
from app_mailreg.models import *


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
            return bcrypt.verify(self.password, self.userdb.hash)
        except Exception:
            return False

    def __init__(self, id, password=None, userdb=None):
        self.id = unicode(id)
        self.userdb = userdb if userdb else UserDB.query.filter_by(
            name_user=self.id).first()
        self.anonymous = False if self.userdb else True
        self.password = password


@login_manager.user_loader
def load_user(id):
    u = UserDB.query.filter_by(name_user=id).first()
    return User(u.name_user, userdb=u) if u else None


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        u = User(request.form["username"], password=request.form["password"])
        if u.anonymous:
            flash("Login failed: username not recognized or invalid password")
        else:
            if u.authenticate():
                login_user(u, remember=True)
                flash("Login successful")
                return redirect(url_for("index"))
            else:
                flash("Login failed: username not recognized or invalid password")
    return render_template("login.html", user=current_user, form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You had been logged out")
    return redirect(url_for("index"))

login_manager.login_view = "login"


@app.route("/")
def index():
    return render_template("base_template.html", current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        flash("Registration successful")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/admin")
@login_required
def admin():
    return ""


@app.route("/favicon.ico")
def favicon():
    """Fallback for serving favicon.ico on older browsers not supporting
    <link> tags and expecting the icon file from application root.

    """
    return send_from_directory(
        path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon")
