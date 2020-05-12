from flask import Flask, Blueprint, request, jsonify, render_template, session, flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app
from flask_api import myConnection
from forms import RegistrationForm, LoginForm, BookingForm
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
        url=("http://127.0.0.1:5000/login/")
        response=requests.post(url,json=request.form)
        response=response.text
        if response:
            response=response.strip("\"")
            response=response.strip("\"")
        if "2" in response:    
                session['email']=form.email.data
                print("Session set")
                return redirect(url_for('site.home'))
        elif "3" in response:
                flash(f'Password is incorrect','danger')
        else:
            flash(f'Username not found','danger')
    return render_template('login.html', title='Login', form=form)



@site.route("/home",methods=['GET','POST'])
def home():
    url=("http://127.0.0.1:5000/orderhistory/"+session['email'])
    response=requests.get(url)
    orderhistory=json.loads(response.text)
    url=("http://127.0.0.1:5000/confirmedbookings/"+session['email'])
    response=requests.get(url)
    confirmedbookings=json.loads(response.text)
    url=("http://127.0.0.1:5000/cars")
    response=requests.get(url)
    availablecars=json.loads(response.text)
    if request.method=='POST':
        if ('find' in request.form):
            print(request.form['search'])
            url=("http://127.0.0.1:5000/searchcar/"+request.form['search'])
            response=requests.get(url)
            searchcars=json.loads(response.text)
            if searchcars:
                return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=searchcars,confirmedbookings=confirmedbookings)
            else:
                return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None,confirmedbookings=confirmedbookings)
        else:
            return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None,confirmedbookings=confirmedbookings)

    return render_template('home.html',title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,confirmedbookings=confirmedbookings)

@site.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('site.login'))

@site.route("/booking",methods=['GET','POST'])
def booking():
    form=BookingForm()
    if request.method=="POST":
        if('carid' in request.form):
                return render_template("booking.html",title='Booking Car', carid=request.form['carid'],username=session['email'],datetime=None,form=form)
        if('booked' in request.form):
                if(request.form['pickup']>request.form['dropoff']):
                    error=True
                    return render_template("booking.html",title='Booking Car',carid=request.form['rego'], username=session['email'],error=error,form=form)
                result=json.dumps(request.form)
                result=json.loads(result)
                url="http://127.0.0.1:5000/bookcar"
                response=requests.post(url, json=result)
                response=response.text
                if response:
                    response=response.strip("\"")
                    response=response.strip("\"")
                if "Vehicle Booked" in response:
                    flash(f'Booking Successful', 'success')
                    return redirect(url_for('site.home'))
                else:
                    flash(f'Booking cannot be made, please try again later or with a different car/dates\nWe apologise for inconvenience caused','danger')
                    return response
        elif ('goback' in request.form):
            return redirect(url_for('site.home'))

    return render_template("booking.html",title='Booking Car',carid=None, username=session['email'],form=form)

@site.route("/about",methods=['GET','POST'])
def about():
    return render_template("about.html")