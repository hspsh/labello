import logging

from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from labello.database import db, Label
from labello.templating.loader import jinja_env as label_tpl, get_variables

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__,
                        template_folder='templates')

@api.route('/', defaults={'page': 'index'})
@api.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
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
    
    return jsonify({
        'variables': sorted(label_vars)
    })


    