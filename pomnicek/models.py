from sqlalchemy import Table, Column, ForeignKey, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_security import UserMixin, RoleMixin

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


class Submit(Base):
    __tablename__ = "submits"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)

    date_for = Column(DateTime, primary_key=True)

    submits = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, submits: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.submits = submits

    def __repr__(self):
        return f"<Submit {self.timestamp} from {self.date_for} with {self.submits} submits>"


class Vaccine(Base):

    __tablename__ = "vaccines"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)

    date_for = Column(DateTime, primary_key=True)

    first_vaccines = Column(Integer, index=False, unique=False, nullable=False)

    second_vaccines = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, first_vaccines: int, second_vaccines: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.first_vaccines = first_vaccines
        self.second_vaccines = second_vaccines

    def __repr__(self):
        return (
            f"<Vaccine {self.timestamp} from {self.date_for} with {self.first_vaccines} and "
            + f"{self.second_vaccines} vaccines"
        )


class Dead(Base):

    __tablename__ = "deads"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)

    date_for = Column(DateTime, primary_key=True)

    deads_cumulative = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, deads_cumulative: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.deads_cumulative = deads_cumulative

    def __repr__(self):
        return f"<Dead {self.timestamp} from {self.date_for} with {self.deads_cumulative} deaths"


class Case(Base):

    __tablename__ = "cases"

    timestamp = Column(DateTime, index=False, unique=False, nullable=False)

    date_for = Column(DateTime, primary_key=True)

    cases = Column(Integer, index=False, unique=False, nullable=False)

    cases_cumulative = Column(Integer, index=False, unique=False, nullable=False)

    def __init__(self, timestamp: datetime, date_for: datetime, cases: int, cases_cumulative: int):
        self.timestamp = timestamp
        self.date_for = date_for
        self.cases = cases
        self.cases_cumulative = cases_cumulative

    def __repr__(self):
        return f"<Case {self.timestamp} from {self.date_for} with {self.cases} cases"
