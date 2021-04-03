from flask import Blueprint, json, request, current_app, abort

from .models import Dead, Story, Message


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
    def remove(d):
        from copy import copy

        dd = copy(d)
        del dd["contact_email"]
        del dd["public"]
        return dd

    request_api_key = request.args.get("api_key", "")
    if request_api_key != current_app.config["API_KEY"]:
        abort(403)

    stories = [remove(d.to_dict()) for d in Story.query.filter(Story.public).order_by(Story.date.desc()).all()]
    return jsonify(stories)


@bp.route("/messages", methods=["GET"])
def messages():
    messages = [d.to_dict() for d in Message.query.order_by(Message.date.desc()).all()]
    return jsonify(messages)
