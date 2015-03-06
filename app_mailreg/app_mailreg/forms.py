from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
from flask.ext.wtf.recaptcha import RecaptchaField
from wtforms.fields import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from wtforms.validators import Email as EmailValidator
from wtforms.validators import Length as LengthValidator


__all__ = ["LoginForm", "RegisterForm"]


class LoginForm(Form):
    username = TextField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField("Username", validators=[DataRequired()])
    email = EmailField("Email",  validators=[DataRequired(), EmailValidator()])
    email_verify = EmailField("Verify Email",  validators=[DataRequired(), EqualTo("email")])
    password = PasswordField("Password", validators=[DataRequired(), LengthValidator(min=8)])
    password_verify = PasswordField(
        "Verify Password", validators=[DataRequired(), EqualTo("password")])
    #recaptcha = RecaptchaField(validators=[Recaptcha()])
