__version__ = "0.0.1"
import logging
import os
import subprocess
import tempfile
from datetime import datetime

from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    url_for,
    request,
    jsonify,
    abort,
)

from labello import settings
from labello.database import db, Label
from labello.label_templating import env as label_tpl, get_variables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 69420

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

common_vars_tpl = {
    "version": __version__,
    "site_name": settings.name,
    "base_url": settings.base_url,
}


@app.before_request
def before_request():
    app.logger.debug("connecting to db")
    db.connect()


@app.teardown_appcontext
def after_request(error):
    app.logger.debug("closing db")
    db.close()


def send_raw_to_printer(data, printer):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epl") as fp:
        fp.write(data.encode())
        fp.write("\n\n".encode())
        command = "lp -h 192.168.88.119:631 -d {} -o raw {}".format(printer, fp.name)
    logger.info(command)
    res = subprocess.call(command, shell=True)
    return res


@app.route("/")
def gallery():
    labels = Label.select()
    return render_template("label_gallery.html", labels=labels, **common_vars_tpl)


@app.route("/editor/new", methods=["GET", "POST"])
@app.route("/editor/<label_id>", methods=["GET", "POST"])
def label_editor(label_id=None):
    """Edit or create labels"""
    if request.method == "POST" and request.values.get("raw"):
        data = request.values.get("raw")
        if request.values.get("print"):
            res = send_raw_to_printer(data, settings.printer_name)
            flash(
                f"sent {len(data)} bytes to printer {settings.printer_name}",
                "success" if res == 0 else "error",
            )
        elif request.values.get("save"):
            if label_id is None:
                new_label = Label.create(raw=data, last_edit=datetime.now())
                new_label.save()
                return redirect(url_for("label_editor", label_id=new_label.id))
            else:
                label = Label.select().where(Label.id == label_id).get()
                label.raw = data
                label.last_edit = datetime.now()
                label.save()

    if label_id is not None:
        label = Label.select().where(Label.id == label_id).get()
        if label:
            return render_template(
                "editor.html", raw=label.raw, label_id=label_id, **common_vars_tpl
            )
    return render_template("editor.html", raw="", label_id=label_id, **common_vars_tpl)

def sub_dict(somedict, somekeys, default=None):
    return dict([ (k, somedict.get(k, default)) for k in somekeys ])

@app.route("/print/<label_id>", methods=["GET", "POST"])
def print_template(label_id):
    label_vars = get_variables(label_tpl, label_id)
    if request.method == "POST":
        label_ctx = sub_dict(request.form, label_vars, default="")
    else:
        label_ctx = sub_dict(request.values, label_vars, default="")

    template = label_tpl.loader.load(label_tpl, label_id)
    rendered = template.render(label_ctx)

    if request.method == "POST" and request.values.get("preview"):
        print(label_ctx)
        return redirect(url_for('print_template', label_id=label_id, **label_ctx))

    if request.method == "POST" and request.values.get("print"):
        data = rendered
        res = send_raw_to_printer(data, settings.printer_name)
        flash(
            f"sent {len(data)} bytes to printer {settings.printer_name}",
            "success" if res == 0 else "error",
        )
    return render_template(
        "print.html",
        rendered=rendered,
        label_id=label_id,
        label_vars=label_ctx,
        **common_vars_tpl,
    )


@app.route("/send_raw", methods=["GET", "POST"])
def send_raw():
    """Send raw text to printer"""
    if request.method == "POST" and request.values.get("raw"):
        data = request.values.get("raw")
        res = send_raw_to_printer(data, settings.printer_name)
        flash(
            f"sent {len(data)} bytes to printer {settings.printer_name}",
            "success" if res == 0 else "error",
        )

    return render_template(
        "send_raw.html", printer_name=settings.printer_name, **common_vars_tpl
    )
