import datetime

from .database import db
from flask_admin.babel import lazy_gettext as _
from flask_security.core import RoleMixin, UserMixin
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    event,
    func,
    text,
)
from sqlalchemy.orm import backref, declarative_mixin, registry, relationship


@declarative_mixin
class TimestampMixin:
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now,
        nullable=False,
        name=_("created_at"),
    )
    modified_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now,
        nullable=False,
        name=_("modified_at"),
    )


class RolesUsers(db.Model):
    __tablename__ = "security_roles_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey("firenze_user.id"))
    role_id = db.Column("role_id", db.Integer(), db.ForeignKey("security_role.id"))


class Role(db.Model, RoleMixin, TimestampMixin):
    __tablename__ = "security_role"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text(), nullable=True)
    permissions = db.Column(db.JSON(), nullable=True)

    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception
    # TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin, TimestampMixin):
    __tablename__ = "firenze_user"

    id = Column(Integer(), primary_key=True)
    username = Column(String(64), unique=True, nullable=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean(), default=True)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    last_login_at = Column(DateTime(timezone=True))
    current_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(String(64))
    current_login_ip = Column(String(64))
    login_count = Column(Integer())

    roles = relationship(
        "Role",
        secondary="security_roles_users",
        backref=backref("users", lazy="dynamic"),
    )

    def __str__(self):
        return self.username


class Comuna(db.Model, TimestampMixin):
    __tablename__ = "ferias_comuna"

    id = Column(Integer(), primary_key=True)
    slug = Column(String(64), unique=True)
    nombre = Column(String(64))
    cut = Column(Integer())
    provincia = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    ubicacion = Column(db.JSON(), nullable=True)

    def __str__(self):
        return self.slug


class Feria(db.Model, TimestampMixin):
    __tablename__ = "ferias_feria"

    id = Column(Integer(), primary_key=True)
    slug = Column(String(64), unique=True)
    nombre = Column(String(64))
    lunes = Column(Boolean(), default=False)
    martes = Column(Boolean(), default=False)
    miercoles = Column(Boolean(), default=False)
    jueves = Column(Boolean(), default=False)
    viernes = Column(Boolean(), default=False)
    sabado = Column(Boolean(), default=False)
    domingo = Column(Boolean(), default=False)
    ubicacion = Column(db.JSON(), nullable=True)
    comuna_id = Column("comuna_id", db.Integer(), db.ForeignKey("ferias_comuna.id"))

    def __str__(self):
        return self.slug
