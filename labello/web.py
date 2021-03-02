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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 69420

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

common_vars_tpl = {"version": __version__, "site_name": settings.name, "base_url": settings.base_url}

@app.before_request
def before_request():
    app.logger.debug("connecting to db")
    db.connect()


@app.teardown_appcontext
def after_request(error):
    app.logger.debug("closing db")
    db.close()

def send_raw_to_printer(data, printer):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.epl') as fp:
        fp.write(data.encode())
        fp.write("\n\n".encode())
        command = "lp -h 192.168.88.119:631 -d {} -o raw {}".format(printer, fp.name)
    logger.info(command)
    res = subprocess.call(command, shell = True)
    return res

@app.route("/")
def gallery():
    labels = Label.select()
    return render_template(
        "label_gallery.html",
        labels=labels,
        **common_vars_tpl
    )

@app.route("/editor", methods=["GET", "POST"])
def send_raw():
    """Edit or create labels"""
    if request.method == "POST" and request.values.get("raw"):
        data = request.values.get("raw")
        _id = request.values.get("id", None)

    return render_template(
        "editor.html",
        **common_vars_tpl
    )

@app.route("/send_raw", methods=["GET", "POST"])
def send_raw():
    """Send raw text to printer"""
    if request.method == "POST" and request.values.get("raw"):
        data = request.values.get("raw")
        res = send_raw_to_printer(data, settings.printer_name)
        flash(f"sent {len(data)} bytes to printer {settings.printer_name}", "success" if res == 0 else "error")

    return render_template(
        "send_raw.html",
        printer_name=settings.printer_name,
        **common_vars_tpl
    )


