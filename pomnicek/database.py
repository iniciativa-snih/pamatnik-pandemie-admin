import click
from flask import current_app as app
from flask.cli import with_appcontext
from datetime import date
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
    from .models import Dead, Story, Role, User  # noqa: F401

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

    db_session.add(Story(date=date(2021, 3, 8), name=u"Jana P.", story=u"Učitelka na ZŠ", age=55, city=u"Praha"))
    db_session.add(
        Story(date=date(2021, 3, 7), name=u"Petr A.", story=u"Učitel na VŠ", age=45, city=u"České Budějovice")
    )
    db_session.add(
        Story(date=date(2021, 3, 7), name=u"Karel Kotvald", story=u"Strojař", age=45, city=u"Hradec Králové")
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
