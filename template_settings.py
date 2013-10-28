from datetime import timedelta

# flask

SECRET_KEY = "string"


# flask-login - login/logout

SESSION_PROTECTION = "strong"

REMEMBER_COOKIE_DURATION = timedelta(days=90)


# flask-wtf - forms

CSRF_ENABLED = True


# py-bcrypt - password hashing

BCRYPT_WORKFACTOR = 14


# database

DB_HOST = "host"
DB_PORT = 5432
DB_SCHEMA = "schema"
DB_USER = "user"
DB_PASSWORD = "password"


# flask-sqlalchemy - database ORM

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA)

# recaptcha

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = "public_key"
RECAPTCHA_PRIVATE_KEY = "private_key"

# random

NTOKEN_RANDOM_BITS = 192
