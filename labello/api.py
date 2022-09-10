import logging

from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from labello.database import db, Label
from labello.templating import epl
from labello.templating.loader import jinja_env as label_tpl, get_variables
from labello import printer, settings

logger = logging.getLogger(__name__)

api = Blueprint("api", __name__, template_folder="templates")


@api.route("/", defaults={"page": "index"})
@api.route("/<page>")
def show(page):
    try:
        return render_template(f"pages/{page}.html")
    except TemplateNotFound:
        abort(404)


@api.route("/label/<label_id>/print", methods=["GET"])
def fields(label_id):
    label = Label.select().where(Label.id == label_id)
    if label:
        label = label.get()
    else:
        return abort(404)
    try:
        label_vars = get_variables(label_tpl, label_id)
    except Exception as exc:
        logger.error(exc)
        label_vars = {}

    return jsonify({"variables": sorted(label_vars)})


# TODO: code duplication :)
def sub_dict(somedict, somekeys, default=None):
    return dict([(k, somedict.get(k, default)) for k in somekeys])


@api.route("/label/<label_id>/print", methods=["POST"])
def print(label_id):
    label = Label.select().where(Label.id == label_id)
    if label:
        label = label.get()
    else:
        return abort(404)
    try:
        label_vars = get_variables(label_tpl, label_id)
    except Exception as exc:
        logger.error(exc)
        label_vars = {}

    label_ctx = sub_dict(request.form, label_vars, default="")

    try:
        template = label_tpl.loader.load(label_tpl, label_id)
        # TODO: why are we not inhereting globals from jinja_env? fix this
        template.globals.update(epl=epl)
        rendered_epl = template.render(label_ctx)
    except Exception as exc:
        logger.error(exc)
        rendered_epl = None
        return

    res = printer.send_raw(rendered_epl, settings.printer_name)
    return res
