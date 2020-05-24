"""
.. module:: flask_main

"""
# python3 flask_main.py
import os
from config import app
from flask_api import api
from flask_site import site

basedir = os.path.abspath(os.path.dirname(__file__))


app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
