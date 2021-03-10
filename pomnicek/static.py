from flask import Blueprint

from flask import render_template, send_from_directory, request
from flask import current_app as app


bp = Blueprint("static", __name__)


@bp.route("/")
def index():
    return render_template("index.jinja2")


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
