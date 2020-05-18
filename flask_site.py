from flask import Flask, Blueprint, request, jsonify, render_template, session, flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app
from flask_api import myConnection
from forms import RegistrationForm, LoginForm, BookingForm
from login import new_user, logon, verify_register, verify_password
import os, requests, json
from datetime import datetime



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
        if response.__contains__("success"):
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
        url=("http://127.0.0.1:5000/hashme")
        password=requests.post(url, json=request.form)
        password=password.text
        password=password.replace("\n",'')
        password=password.replace('"','')
        data={"email":request.form["email"],"password": password}
        url=("http://127.0.0.1:5000/login")
        response=requests.post(url,json=data)
        response=response.text
        if response.__contains__("success"):    
                session['email']=form.email.data
                print("Session set")
                return redirect(url_for('site.home'))
        elif response.__contains__("password incorrect"):
                flash(f'Password is incorrect','danger')
        else:
            flash(f'Username not found','danger')
    return render_template('login.html', title='Login', form=form)



@site.route("/home",methods=['GET','POST'])
def home():
    url=("http://127.0.0.1:5000/username/"+session['email'])
    response=requests.get(url)
    username=json.loads(response.text)
    url=("http://127.0.0.1:5000/orderhistory/"+session['email']) #API call to fetch booking history of the logged in customer
    response=requests.get(url)
    orderhistory=json.loads(response.text)
    url=("http://127.0.0.1:5000/confirmedbookings/"+session['email']) #API call to fetch confirmed bookings of the logged in customer to be able to display on cancel page
    response=requests.get(url)
    confirmedbookings=json.loads(response.text)
    url=("http://127.0.0.1:5000/cars") #API call to fetch available cars' list
    response=requests.get(url)
    availablecars=json.loads(response.text)
    if request.method=='POST':
        if ('find' in request.form):
            url=("http://127.0.0.1:5000/searchcar/"+request.form['search'])
            response=requests.get(url)
            searchcars=json.loads(response.text)
            if searchcars:
                return render_template('home.html',user=username,title='Home',orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=searchcars,confirmedbookings=confirmedbookings)
            else:
                return render_template('home.html',title='Home',user=username,orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None,confirmedbookings=confirmedbookings)
            #If Customer tries to cancel a booking
        elif ('cancel' in request.form):
                if len(request.form)>1: 
                    list=request.form.getlist('bookingnumber')
                    result=json.dumps(list)
                    result=json.loads(result)
                    url=("http://127.0.0.1:5000/cancelbooking/email="+session['email'])
                    response=requests.post(url, json=result)
                    response=response.text
                    if response:
                        response=response.replace('"',"")
                        response=response.replace("\n","")
                    print("This is the cancellation response")
                    print(response)
                    print("\n\n\n")
                    if response.__contains__("Booking successfully cancelled"):
                        flash(f'Booking Cancelled', 'success')
                        url=("http://127.0.0.1:5000/confirmedbookings/"+session['email']) #API call to fetch confirmed bookings of the logged in customer to be able to display on cancel page
                        response=requests.get(url)
                        confirmedbookings=json.loads(response.text)
                        return render_template('home.html',title='Home',user=username,orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None,confirmedbookings=confirmedbookings)
                    else:
                        flash(response,'danger')
                else:
                   flash(f'No Booking selected for cancllation','danger')

        else:
            return render_template('home.html',title='Home',user=username,orderhistory=orderhistory, booking=None,availablecars=availablecars,searchcars=None,confirmedbookings=confirmedbookings)
    print("\n\n\n")
    return render_template('home.html',title='Home',user=username,orderhistory=orderhistory, booking=None,availablecars=availablecars,confirmedbookings=confirmedbookings)

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
                now = datetime.now()
                pickup=datetime.strptime(request.form['pickup'],'%Y-%m-%dT%H:%M')
                if(now>pickup):
                    pickuperror=True
                    return render_template("booking.html",title='Booking Car',carid=request.form['rego'], username=session['email'],pickuperror=pickuperror,form=form,dropofferror=False)
                if(request.form['pickup']>request.form['dropoff']):
                    dropofferror=True
                    return render_template("booking.html",title='Booking Car',carid=request.form['rego'], username=session['email'],dropofferror=dropofferror,form=form,pickuperror=False)
                result=json.dumps(request.form)
                result=json.loads(result)
                url="http://127.0.0.1:5000/bookcar"
                response=requests.post(url, json=result)
                response=response.text
                if response:
                    response=response.strip("\"")
                    response=response.strip("\"")
                if response.__contains__("Vehicle Booked"):
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