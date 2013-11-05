from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import *

from app_mailreg import db


__all__ = ["UserDB", "UserContact", "ContactPhone", "ContactEmail", "UserNotification"]


class UserDB(db.Model):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("name_user", name="ix_name_user"), {"schema": "public"})

    id_user = Column("id_user", INTEGER, Sequence("user_id", 1, 1), primary_key=True)
    _name_user = Column("name_user", VARCHAR, unique=True, nullable=False)
    hash = Column(CHAR(60), nullable=True, server_default=text("NULL"))
    is_active = Column(BOOLEAN, nullable=False, server_default=text("TRUE"))
    is_verified = Column(BOOLEAN, nullable=False, server_default=text("FALSE"))
    is_resetforced = Column(BOOLEAN, nullable=False, server_default=text("FALSE"))
    is_resetrequested = Column(BOOLEAN, nullable=False, server_default=text("FALSE"))
    timestamp_create = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    contact = relationship("UserContact", backref=backref("user", uselist=False))
    record_usernotification = relationship("UserNotification", backref=backref("user"))
    record_userlogin = relationship("UserLogin", backref=backref("user"))

    @hybrid_property
    def name_user(self):
        return self._name_user

    @name_user.setter
    def name_user(self, value):
        if value:
            self._name_user = value.strip().lower()
        else:
            self._name_user = None

    def __init__(self, name_user, **kwargs):
        self.name_user = name_user

        try:
            self.hash = kwargs["hash"]
        except KeyError:
            self.hash = None


class UserContact(db.Model):
    __tablename__ = "contact"
    __table_args__ = (UniqueConstraint("id_user", name="ix_id_user-contact"), {"schema": "public"})

    id_contact = Column(INTEGER, Sequence("contact_id", 1, 1), primary_key=True)
    id_user = Column(
        INTEGER, ForeignKey("public.user.id_user", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    _name_last = Column("name_last", VARCHAR, nullable=True)
    _name_first = Column("name_first", VARCHAR, nullable=False, server_default=text("'noname'"))
    name_prefix = Column(VARCHAR, nullable=True)
    name_suffix = Column(VARCHAR, nullable=True)
    position = Column(VARCHAR, nullable=True)
    company = Column(VARCHAR, nullable=True)
    industry = Column(VARCHAR, nullable=True)
    # Implement website as one-off field for now.
    website = Column(VARCHAR, nullable=True, server_default=text("NULL"))

    record_phone = relationship("ContactPhone", backref=backref("contact"))
    record_email = relationship("ContactEmail", backref=backref("contact"))

    @hybrid_property
    def name_last(self):
        return self._name_last

    @name_last.setter
    def name_last(self, value):
        if value:
            self._name_last = value.strip()
        else:
            self._name_last = None

    @hybrid_property
    def name_first(self):
        return self._name_first

    @name_first.setter
    def name_first(self, value):
        if value:
            self._name_first = value.strip()
        else:
            self._name_first = "noname"

    @hybrid_property
    def name(self):
        x = (
            self.name_prefix if self.name_prefix else "",
            self._name_first,
            self._name_last if self._name_last else "",
            self.name_suffix if self.name_suffix else "")
        return " ".join(x).strip()

    def __init__(self, id_user, name_first, name_last=None, **kwargs):
        self.id_user = id_user
        self.name_last = name_last
        self.name_first = name_first


PHONE_TYPES = ("mobile", "home", "office", "fax")


class ContactPhone(db.Model):
    __tablename__ = "phone"
    __table_args__ = (
        UniqueConstraint(
            "id_contact", "code_country", "code_area", "number", "extension",
            name="ix_id_contact-phone"),
        {"schema": "public"})
        # TODO: Introduce db constraint of only one phone default per contact.

    id_phone = Column(INTEGER, Sequence("phone_id", 1, 1), primary_key=True)
    id_contact = Column(
        INTEGER, ForeignKey("public.contact.id_contact", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    code_country = Column(INTEGER, nullable=False, server_default=text("0"))
    code_area = Column(INTEGER, nullable=False, server_default=text("0"))
    number = Column(INTEGER, nullable=False, server_default=text("0"))
    extension = Column(INTEGER, nullable=True, server_default=text("NULL"))
    type_ = Column(
        "type", ENUM(*PHONE_TYPES, name="phone_types"), nullable=False,
        server_default=text("'mobile'"))
    is_default = Column(BOOLEAN, nullable=False, server_default=text("FALSE"))

    def __init__(self, id_contact, number, phone_type="mobile",
                 code_country=0, code_area=0, extension=None, default=True):
        self.id_contact = id_contact
        self.number = number
        self.code_country = code_country
        self.code_area = code_area
        self.extension = extension
        if phone_type in PHONE_TYPES:
            self.type_ = phone_type
        else:
            raise ValueError("{0} is not a valid phone type".format(phone_type))
        self.is_default = default


EMAIL_TYPES = ("personal", "work")


class ContactEmail(db.Model):
    __tablename__ = "email"
    __table_args__ = (
        UniqueConstraint("id_contact", "email", name="ix_id_contact-email"), {"schema": "public"})
        # TODO: Introduce db constraint of only one email default per contact.

    id_email = Column(INTEGER, Sequence("email_id", 1, 1), primary_key=True)
    id_contact = Column(
        INTEGER, ForeignKey("public.contact.id_contact", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    email = Column(VARCHAR, nullable=False)
    type_ = Column(
        "type", ENUM(*EMAIL_TYPES, name="=email_types"),
        nullable=False, server_default=text("'personal'"))
    is_default = Column(BOOLEAN, nullable=False, server_default=text("FALSE"))

    def __init__(self, id_contact, email, email_type="personal", default=True):
        self.id_contact = id_contact
        self.email = email
        if email_type.lower() in EMAIL_TYPES:
            self.type_ = email_type.lower()
        else:
            raise ValueError("{0} is not a valid email type".format(email_type))
        self.is_default = default


USERNOTIFICATION_TYPES = ("verify", "forgot", "reset", "remove")


class UserNotification(db.Model):
    __tablename__ = "user_notification"
    __table_args__ = (
        UniqueConstraint("id_user", "type", name="ix_usernotification"), {"schema": "public"})

    id_usernotification = Column(
        CHAR(60), nullable=True, server_default=text("NULL"), primary_key=True)
    id_user = Column(
        INTEGER, ForeignKey("public.user.id_user", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    type_ = Column(
        "type", ENUM(*USERNOTIFICATION_TYPES, name="=usernotification_types"), nullable=True,
        server_default=text("NULL"))
    timestamp_sent = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, ntoken, id_user, notification_type):
        self.id_usernotification = ntoken
        self.id_user = id_user
        if notification_type.lower() in USERNOTIFICATION_TYPES:
            self.type_ = notification_type.lower()
        else:
            raise ValueError("{0} is not a valid user notification type".format(notification_type))


class UserLogin(db.Model):
    # TODO: Implement anti-DOS features on successful logins.
    __tablename__ = "user_login"
    __table_args__ = ({"schema": "public"})

    id_userlogin = Column(INTEGER, Sequence("userlogin_id", 1, 1), primary_key=True)
    id_user = Column(
        INTEGER, ForeignKey("public.user.id_user", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    ip_login = Column(INET, nullable=True, server_default=text("NULL"))
    timestamp_login = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
