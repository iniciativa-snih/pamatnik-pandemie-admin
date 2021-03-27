import os

from flask import Flask
from flask import url_for
from flask_babel import Babel
from flask_talisman import Talisman

from flask_security import Security, SQLAlchemySessionUserDatastore

from flask_admin import Admin
from flask_admin import helpers as admin_helpers


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False, static_folder="static")

    if test_config is not None:
        config_class = test_config
    elif "APP_SETTINGS" in os.environ:
        config_class = os.environ["APP_SETTINGS"]
    else:
        print("APP_SETTINGS env var is missing config class, provide one")
        exit(1)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # migrate = Migrate(app, db)

    Babel(app)
    csp = {
        "default-src": "'self'",
        "font-src": ["'self'", "fonts.gstatic.com"],
        "style-src": ["'self'", "fonts.googleapis.com"],
        "script-src": ["'self'", "plausible.io"],
        "connect-src": ["'self'", "plausible.io"],
    }
    Talisman(app, content_security_policy=csp)

    with app.app_context():
        from .database import db_session
        from .models import User, Role, Story, Message
        from .admin import AdminModelView, StoryModelView, MessageModelView

        user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
        security = Security(app, user_datastore)

        # Create admin
        admin = Admin(
            app,
            "Památník pandemie",
            base_template="my_master.html",
            template_mode="bootstrap3",
        )

        admin.add_view(StoryModelView(Story, db_session))
        admin.add_view(MessageModelView(Message, db_session))
        admin.add_view(AdminModelView(User, db_session))
        admin.add_view(AdminModelView(Role, db_session))

        # define a context processor for merging flask-admin's template context into the
        # flask-security views.
        @security.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template, admin_view=admin.index_view, h=admin_helpers, get_url=url_for
            )

        from . import init  # noqa: F401
        from .init import init_app

        init_app(app)

        from . import static

        app.register_blueprint(static.bp)

        from . import api

        app.register_blueprint(api.bp, url_prefix="/api")

        return app
