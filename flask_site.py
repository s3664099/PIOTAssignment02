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
@site.route("/register",methods=['GET','POST'])
def register():
    # Use REST API.
    form=RegistrationForm()
    if form.validate_on_submit():
        # encrypt this form.password.data before hitting the api
        result=json.dumps(request.form)
        result=json.loads(result)
        url=("http://127.0.0.1:5000/registeruser")
        response=requests.post(url,json=result)
        response=response.text
        if response:
            response=response.strip("\"")
            response=response.strip("\"")
        print("\n\n******This is in SITE********")
        print(response,"\n\n")
        print(response=="success%")
        if "success" in response:
             flash(f'Account Created', 'success')
             return redirect(url_for('site.login'))
        else:
            flash(f'Username or Email already in use')
            return redirect(url_for('site.register'))
    return render_template("register.html",title="Register", form=form)
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
        if storedpwd:
            storedpwd=storedpwd.strip("\"")
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
    if request.method=='POST':
        if ('find' in request.form):
            print(request.form['search'])
            url=("http://127.0.0.1:5000/searchcar/"+request.form['search'])
            response=requests.get(url)
            print("\n\n Order History \n\n")
            print(response)
            searchcars=json.loads(response.text)
            if searchcars:
                return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=searchcars)
            else:
                return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None)
        else:
            return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None)

    return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars)

@site.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('site.login'))

@site.route("/about",methods=['GET','POST'])
def about():
    return render_template("about.html")