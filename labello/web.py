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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 69420

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

common_vars_tpl = {"version": __version__, "site_name": settings.name, "base_url": settings.base_url}

def send_raw_to_printer(data, printer):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.epl') as fp:
        fp.write(data.encode())
        fp.write("\n\n".encode())
        command = "lp -h 192.168.88.119:631 -d {} -o raw {}".format(printer, fp.name)
    logger.info(command)
    res = subprocess.call(command, shell = True)
    return res


@app.route("/", methods=["GET", "POST"])
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


