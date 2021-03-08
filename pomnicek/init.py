from datetime import datetime

import click
from flask import current_app as app
from flask.cli import with_appcontext

from .database import init_db_command
from .update import update


@click.command("update")
@with_appcontext
def update_command():
    update()
    click.echo("Database updated.")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(update_command)


@app.template_filter()
def fmt_number(value):
    # https://stackoverflow.com/q/36889758/5763764
    return "{0:,}".format(value).replace(",", "&thinsp;")


@app.template_filter()
def fmt_date(value):
    return datetime.strftime(value, "%d. %m. %Y").lstrip("0").replace(" 0", " ")


app.jinja_env.filters["fmt_number"] = fmt_number
app.jinja_env.filters["fmt_date"] = fmt_date
