from sqlalchemy import Table, Column, ForeignKey, Integer, DateTime, String, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_security import UserMixin, RoleMixin

from sqlalchemy_serializer import SerializerMixin

from .database import Base


user_role_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)


class Role(Base, RoleMixin):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return f"<Role {self.id}, {self.name}, {self.description}"


class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean)
    confirmed_at = Column(DateTime)
    roles = relationship("Role", secondary=user_role_table)


class Dead(Base, SerializerMixin):
    __tablename__ = "dead"

    date = Column(Date, primary_key=True)
    daily = Column(Integer, index=False, unique=False, nullable=False)
    cumulative = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, date: datetime, daily: int, cumulative: int):
        self.date = date
        self.daily = daily
        self.cumulative = cumulative

    def __repr__(self):
        return f"<Deads for {self.date} {self.daily}, cumulative {self.cumulative}"


class Story(Base, SerializerMixin):
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    story = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String, nullable=True)
    statue = Column(String, nullable=False)


class Message(Base, SerializerMixin):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    message = Column(String, nullable=False)
