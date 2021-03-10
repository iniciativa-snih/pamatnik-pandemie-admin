import os
import pytest
from datetime import date

from pomnicek import create_app


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")

    with app.app_context():
        from pomnicek.database import init_db, db_session

        init_db()

        from pomnicek.models import Story

        db_session.add(Story(date=date.today(), name="Aleš M.", story="Soustružník", age=78, city="Hradec Králové"))
        db_session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
