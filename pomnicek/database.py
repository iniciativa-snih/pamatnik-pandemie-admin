import click
from flask import current_app as app
from flask.cli import with_appcontext
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask_security.utils import encrypt_password


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import string
    import random
    from .models import Submit, Vaccine, Dead, Case, Role, User  # noqa: F401

    Base.metadata.create_all(bind=engine)

    user_role = Role(name="user")
    super_user_role = Role(name="superuser")
    db_session.add(user_role)
    db_session.add(super_user_role)
    db_session.commit()

    admin_user = User(
        first_name="Admin",
        email="admin",
        password=encrypt_password("admin"),
        active=True,
        roles=[user_role, super_user_role],
    )
    db_session.add(admin_user)

    first_names = [
        "Harry",
        "Amelia",
        "Oliver",
        "Jack",
        "Isabella",
        "Charlie",
        "Sophie",
        "Mia",
        "Jacob",
        "Thomas",
        "Emily",
        "Lily",
        "Ava",
        "Isla",
        "Alfie",
        "Olivia",
        "Jessica",
        "Riley",
        "William",
        "James",
        "Geoffrey",
        "Lisa",
        "Benjamin",
        "Stacey",
        "Lucy",
    ]
    last_names = [
        "Brown",
        "Smith",
        "Patel",
        "Jones",
        "Williams",
        "Johnson",
        "Taylor",
        "Thomas",
        "Roberts",
        "Khan",
        "Lewis",
        "Jackson",
        "Clarke",
        "James",
        "Phillips",
        "Wilson",
        "Ali",
        "Mason",
        "Mitchell",
        "Rose",
        "Davis",
        "Davies",
        "Rodriguez",
        "Cox",
        "Alexander",
    ]

    for i in range(len(first_names)):
        tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
        tmp_pass = "".join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
        db_session.add(
            User(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                active=True,
                roles=[
                    user_role,
                ],
            )
        )
    db_session.commit()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@contextmanager
def transaction():
    try:
        yield
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
