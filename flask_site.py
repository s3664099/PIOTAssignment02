from flask import Flask, Blueprint, request, jsonify, render_template, session, flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app
from flask_api import myConnection
from forms import RegistrationForm, LoginForm
from login import new_user, logon, verify_register, verify_password
import os, requests, json

site = Blueprint("site", __name__)


# Client webpage.
@site.route("/register")
def register():
    # Use REST API.
    form=RegistrationForm()
    
    #Needs to be completed 

    return render_template("register.html",title='Register',form=form)


@site.route("/",methods=['GET','POST'])
def login():
    # Use REST API.
    form = LoginForm()    
    if form.validate_on_submit():
        url=("http://127.0.0.1:5000/login/"+form.email.data)
        response=requests.get(url)
        storedpwd = json.loads(response.text)
        storedpwd=storedpwd.strip("\"")
        if storedpwd:
            loggedIn=verify_password(storedpwd,form.password.data)
            if loggedIn==True:
                session['email']=form.email.data
                print("Session set")
                return redirect(url_for('site.home'))
                
            else:
                flash(f'Password is incorrect','danger')
        else:
            flash(f'Username not found','danger')
    return render_template('login.html', title='Login', form=form)


@site.route("/home",methods=['GET','POST'])
def home():
    url=("http://127.0.0.1:5000/orderhistory/"+session['email'])
    response=requests.get(url)
    print("Response",response.text)
    orderhistory=json.loads(response.text)
    
    url=("http://127.0.0.1:5000/cars")
    response=requests.get(url)
    availablecars=json.loads(response.text)

    return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars)

@site.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('site.login'))

@site.route("/about",methods=['GET','POST'])
def about():
    return render_template("about.html")