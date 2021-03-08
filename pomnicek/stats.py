from flask import Blueprint
from datetime import datetime

from flask import render_template, send_from_directory, request
from flask import current_app as app

from .models import Submit, Vaccine, Dead, Case


bp = Blueprint("stats", __name__)


@bp.route("/hello")
def hello():
    return "Hello, world"


@bp.route("/", methods=["GET"])
def index():
    submit = Submit.query.order_by(Submit.date_for.desc()).first()
    date_for = submit.date_for
    date_from = datetime(2020, 12, 27)
    cumulative_date_from = datetime(2020, 12, 26)

    vaccines = Vaccine.query.filter(Vaccine.date_for >= date_from).filter(Vaccine.date_for <= date_for).all()
    vaccinated_no = sum([v.first_vaccines for v in vaccines])

    deads_from = Dead.query.filter(Dead.date_for == cumulative_date_from).first()
    deads_for = Dead.query.filter(Dead.date_for == date_for).first()
    deads_no = deads_for.deads_cumulative - deads_from.deads_cumulative

    cases_from = Case.query.filter(Case.date_for == cumulative_date_from).first()
    cases_for = Case.query.filter(Case.date_for == date_for).first()
    cases_no = cases_for.cases_cumulative - cases_from.cases_cumulative

    return render_template(
        "index.jinja2",
        submit=submit,
        vaccinated=vaccinated_no,
        deads=deads_no,
        date_from=date_from,
        date_for=date_for,
        cases=cases_no,
    )


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
