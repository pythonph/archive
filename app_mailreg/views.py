import os.path as path
from datetime import datetime, date, timedelta


from flask import (
    render_template, Response, request, session, redirect, url_for, flash, send_from_directory, g)
from flask.ext.login import current_user, login_user, logout_user, login_required
from passlib.hash import bcrypt


from app_mailreg import app, login_manager, db
from app_mailreg.forms import *
from app_mailreg.models import *
from app_mailreg.util import User


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

login_manager.login_view = "login"


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        flash("You had been logged out")
        logout_user()
    return redirect(url_for("index"))


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
        path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon")
