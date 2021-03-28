import os

APP_VERSION = "0.1.0"

APP_TITLE = "🏷️ labello"
APP_NAME = "Labello"

APP_BASE_URL = "banana.at.hsp.net.pl:8000"

APP_HOME_URL = "//hsp.sh"
APP_WIKI_URL = "//wiki.hsp.sh/labello"
APP_REPO_URL = "//github.com/hspsh/labello"

printer_name = "Zebra_LP2824"

SECRET_KEY = os.environ["SECRET_KEY"]
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")
