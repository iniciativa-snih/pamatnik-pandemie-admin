from flask import Blueprint

from flask import render_template, send_from_directory, request, flash, redirect
from flask import current_app as app

from wtforms import Form, StringField, IntegerField, validators, DateField
from datetime import datetime

from .database import db_session
from .models import Story

bp = Blueprint("static", __name__)


@bp.route("/")
def index():
    return render_template("index.jinja2")


class StoryForm(Form):
    date = DateField(
        "Datum úmrtí",
        [validators.DataRequired(), validators.InputRequired(message="Zadejte datum úmrtí")],
        format="%d.%m.%Y",
    )
    name = StringField("Jméno", [validators.DataRequired(message="Zadejte jméno")])
    story = StringField("Vzpomínka", [validators.Optional()])
    age = IntegerField("Věk", [validators.Optional()])
    city = StringField("Město", [validators.Optional()])
    contact_email = StringField(
        "Kontaktní email",
        [
            validators.InputRequired(message="Zadejte emailovou adresu"),
            validators.Email(message="Špatná emailová adresa"),
        ],
    )


@bp.route("/pribeh", methods=["GET", "POST"])
def pribeh():
    form = StoryForm(request.form)
    if request.method == "POST" and form.validate():
        story = Story(
            date=form.date.data,
            name=form.name.data,
            story=form.story.data,
            age=form.age.data,
            city=form.city.data,
            statue="none",
            contact_email=form.contact_email.data,
            create_time=datetime.now(),
        )
        db_session.add(story)
        db_session.commit()
        flash("Děkujeme za přidání příběhu. Prosíme o trpělivost než příběh zkontrolujeme a uveřejníme.")
        return redirect("/hotovo")

    return render_template("pribeh.jinja2", form=form)


@bp.route("/hotovo", methods=["GET"])
def hotovo():
    return render_template("hotovo.jinja2")


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/robots.txt")
@app.route("/humans.txt")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja2"), 404
