import os
import pytest
from datetime import date, timedelta

from pomnicek import create_app


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")

    with app.app_context():
        from pomnicek.init import fmt_date, fmt_number

        app.jinja_env.filters["fmt_date"] = fmt_date
        app.jinja_env.filters["fmt_number"] = fmt_number

        from pomnicek.database import init_db, db_session

        init_db()
        db_session.connection().execute("DELETE FROM user")
        db_session.connection().execute("DELETE FROM role")
        db_session.connection().execute("DELETE FROM user_role")
        db_session.connection().execute("DELETE FROM story")
        db_session.connection().execute("DELETE FROM dead")

        from pomnicek.models import Story, Dead

        db_session.add(Story(date=date.today(), name="Aleš M.", story="Soustružník", age=78, city="Hradec Králové"))

        db_session.add(Dead(date=date.today() - timedelta(days=1), daily=100, comulative=300))
        db_session.add(Dead(date=date.today() - timedelta(days=2), daily=50, comulative=200))
        db_session.add(Dead(date=date.today() - timedelta(days=3), daily=50, comulative=150))
        db_session.add(Dead(date=date.today() - timedelta(days=4), daily=100, comulative=100))

        db_session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
