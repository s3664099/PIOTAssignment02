# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_api import api
from flask_site import site
from config import app

basedir = os.path.abspath(os.path.dirname(__file__))


app.register_blueprint(api)
app.register_blueprint(site)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
