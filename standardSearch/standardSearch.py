# Using venv and running app with evironment variable exports and flask command. See below.
# https://flask.palletsprojects.com/en/1.1.x/installation/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/

# Project Setup
# $ mkdir myproject
# $ cd myproject
# $ python3 -m venv venv
# $ . venv/bin/activate

# Flask installation (in venv)
# $ pip install Flask

# Check version (in venv)
# $ flask --version
# Should be Python 3.8.2, Flask 1.1.2, Werkzeug 1.0.1

# If using a development environment (debugging, reloading, etc.):
# $ export FLASK_ENV=development

# Running the app
# $ export FLASK_APP=hello.py
# $ flask run

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

