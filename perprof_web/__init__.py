"""Main file."""


import os

from flask import Flask

# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join("uploads")

# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {"csv", "table"}

app = Flask(__name__)

# pylint: disable=wrong-import-position, disable=cyclic-import
# pyflakes: disable=F401
import perprof_web.views  # isort: skip # noqa

# Configure upload file path flask
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER)

# Define secret key to enable session
app.secret_key = "This is your secret key to utilize session in Flask"
