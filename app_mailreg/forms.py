from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
from flask.ext.wtf.recaptcha import RecaptchaField
from wtforms.fields import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from wtforms.validators import Email as EmailValidator
from wtforms.validators import Length as LengthValidator


__all__ = ["LoginForm", "BaseForm", "RegisterForm"]


class LoginForm(Form):
    username = TextField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(Form):
    username = TextField("Username", validators=[DataRequired()])
    email = EmailField("Email",  validators=[DataRequired(), EmailValidator()])
    email_verify = EmailField(
        "Verify Email",  validators=[DataRequired(), EqualTo("email")])
    password = PasswordField(
        "Password", validators=[DataRequired(), LengthValidator(min=8)])
    password_verify = PasswordField(
        "Verify Password", validators=[DataRequired(), EqualTo("password")])
    #recaptcha = RecaptchaField(validators=[Recaptcha()])


class BaseForm(Form):
    name_prefix = TextField("Prefix")
    name_first = TextField("First Name")
    name_last = TextField("Last Name", validators=[DataRequired()])
    name_suffix = TextField("Suffix")
    position = TextField("Position")
    company = TextField("Company")
    industry = TextField("Industry")
    website = URLField("Website")
    phone_1 = TextField("Phone")
    phone_2 = TextField("Phone Secondary")
    mobile_1 = TextField("Mobile")
    mobile_2 = TextField("Mobile Secondary")
    fax = TextField("Fax")
    email = EmailField("Email")
    email_2 = EmailField("Email Secondary")
