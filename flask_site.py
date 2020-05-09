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


@site.route("/booking", method=['GET','POST'])
def booking():
    # Use REST API
    form = RegisterForm()
    if form.validate_on_submit():
        url=("http://127.0.0.1:5000/booking/"+form.rego.data)
        response=requests.get(url)
        if response:
            (pickup > bookings['pickuptime'] and pickup < bookings['dropofftime'] and bookings['active'] == 1) or (
					dropoff > bookings['pickuptime'] and dropoff < bookings['dropofftime'] and bookings['active'] == 1)
        if response == 1:
            flash ('Vehicle already booked')
            return redirect(url_for('site.booking'))
        
        else:
        flash ('Vehicle Booked, your booking number is "+str(insert_id['LAST_INSERT_ID()'])+" and the price is $"+total_cost')
        return render_template('home.html', title='Booking', form=form) 
        




@site.route("/home",methods=['GET','POST'])
def home():
    url=("http://127.0.0.1:5000/orderhistory/"+session['email'])
    response=requests.get(url)
    orderhistory=json.loads(response.text)
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

@site.route("/booking",methods=['GET','POST'])
def booking():
    form=BookingForm()
    if request.method=="POST":
        print("\n\n Request from home to booking")
        print(request.form)
        print("\n\n")
        if('carid' in request.form):
                return render_template("booking.html",title='Booking Car', carid=request.form['carid'],username=session['email'],form=form)
        if('booked' in request.form):
                result=json.dumps(request.form)
                result=json.loads(result)
                print("\n\n\nBooking Details ")
                print(result)
                print("\n\n\n")
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
            return redirect(url_for(site.home))

    return render_template("booking.html",title='Booking Car',carid=None, username=session['email'],form=form)

@site.route("/about",methods=['GET','POST'])
def about():
    return render_template("about.html")