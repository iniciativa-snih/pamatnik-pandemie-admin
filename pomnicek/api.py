from flask import Blueprint, json, jsonify

from .models import Dead, Story


bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def healt():
    return jsonify("Healthy")


@bp.route("/deads", methods=["GET"])
def deads():
    deads = [d.to_dict() for d in Dead.query.order_by(Dead.date.desc()).all()]
    return jsonify(deads)


@bp.route("/stories", methods=["GET"])
def stories():
    stories = [d.to_dict() for d in Story.query.order_by(Story.date.desc()).all()]
    return json.dumps(stories)
    # return jsonify(stories), 200, {'Content-Type': 'application/json; charset=utf-8'}
