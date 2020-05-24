"""
.. module:: config

"""
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] ='e1cc9668fd15d64484fc8d6f670fb5ca'
app.config['UPLOAD_FOLDER'] = "Images/"