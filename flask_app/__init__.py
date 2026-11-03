import os

from flask import Flask

app = Flask(__name__)
# Set SECRET_KEY in Render's environment settings; the fallback is for local use only.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

from flask_app.config.db import init_db  # noqa: E402

init_db()
