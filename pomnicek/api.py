from flask import Blueprint, json

from .models import Dead, Story


bp = Blueprint("api", __name__)


def jsonify(o):
    return json.dumps(o, ensure_ascii=False).encode("utf8"), 200, {"Content-Type": "application/json; charset=utf-8"}


@bp.route("/health", methods=["GET"])
def health():
    return jsonify("Healthy")


@bp.route("/deads", methods=["GET"])
def deads():
    deads = [d.to_dict() for d in Dead.query.order_by(Dead.date.desc()).all()]
    return jsonify(deads)


@bp.route("/stories", methods=["GET"])
def stories():
    stories = [d.to_dict() for d in Story.query.order_by(Story.date.desc()).all()]
    return jsonify(stories)
