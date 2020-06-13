"""
.. module:: flask_site

"""
from datetime import datetime
#from google.cloud import storage
import json,os,requests
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Blueprint, request, render_template, session, flash, url_for, redirect
from forms import RegistrationForm, LoginForm, BookingForm
#from Encoding.encode_recognise import recognise
from config import app

site = Blueprint("site", __name__)


# Client webpage.
@site.route("/register",methods=['GET','POST'])
def register():
    """
    Registration form from forms.py

    """
    # Use REST API.
    form=RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
                result=json.dumps(request.form)
                result=json.loads(result)
                url=("http://127.0.0.1:5000/registeremployee")
                response=requests.post(url,json=result)
                response=response.text
                if response:
                    response=response.replace('"','')
                    response=response.replace('\n','')
                if response.__contains__("success"):
                    flash(f'Account Created', 'success')
                    return redirect(url_for('site.login'))
                else:
                    flash(f'Username or Email already in use','danger')
                    return redirect(url_for('site.register'))
    return render_template("register.html",title="Register", form=form)

    return render_template("register.html",title='Register',form=form)


@site.route("/",methods=['GET','POST'])
def login():
    """
    Login form from forms.py

    """
    form = LoginForm()
    # Use REST API.
    if request.method=="POST":
        if form.validate_on_submit():
            url=("http://127.0.0.1:5000/role/"+request.form['role']+"/"+request.form['email'])
            role=requests.get(url)
            role=role.text
            role=role.replace("\n",'')
            role=role.replace('"','')
            if role != 'Success':
                flash(f'The selected role is not applicable to the provided email, please validate email and role','danger')
                return render_template('login.html',title='Login',form=form)
            else:
                session['role']=request.form['role']
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
                    if(session['role']=='Admin'):
                        return redirect(url_for('site.admin'))
                    elif(session['role']=='Manager'):
                        return redirect(url_for('site.manager'))
                    elif(session['role']=='Engineer'):
                        return redirect(url_for('site.engineer'))
                    elif(session['role']=='Customer'):
                        return redirect(url_for('site.home'))
                    else:
                        return redirect(url_for('site.home'))
            elif response.__contains__("password incorrect"):
                    flash(f'Password is incorrect','danger')
            else:
                flash(f'Username not found','danger')
    return render_template('login.html', title='Login', form=form)



@site.route("/home",methods=['GET','POST'])
def home():
    """
    Home page

    """
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
    return render_template('home.html',title='Home',user=username,orderhistory=orderhistory, booking=None,availablecars=availablecars,confirmedbookings=confirmedbookings)

@site.route("/admin",methods=['GET','POST'])
def admin():
    form=RegistrationForm()
    url=("http://127.0.0.1:5000/username/"+session['email'])
    response=requests.get(url)
    username=json.loads(response.text)
    url=("http://127.0.0.1:5000/users")
    response=requests.get(url)
    users=json.loads(response.text)
    url=("http://127.0.0.1:5000/getallcars")
    response=requests.get(url)
    cars=json.loads(response.text)
    url=("http://127.0.0.1:5000/unservicedcars")
    response=requests.get(url)
    unservicedcars=json.loads(response.text)
    response=requests.get("http://127.0.0.1:5000/servicehistory")
    servicehistory=json.loads(response.text)
    if form.validate_on_submit():
        if 'add' in request.form:
                result=json.dumps(request.form)
                result=json.loads(result)
                url=("http://127.0.0.1:5000/registeremployee")
                response=requests.post(url,json=result)
                response=response.text
                if response:
                    response=response.replace('"','')
                    response=response.replace('\n','')
                if response.__contains__("success"):
                    flash(f'Account Created', 'success')
                    return redirect(url_for('site.admin'))
                else:
                    flash(f'Username or Email already in use','danger')
                    return redirect(url_for('site.admin'))
        if 'find' in request.form:
            if(request.form['search'] == ''):
                flash(f'Please Enter Car Rego To Search','danger')
                return render_template("admin.html",title='Admin',unservicedcars=unservicedcars,servicehistory=servicehistory,cars=cars,users=users,user=username, rentalhistory=None,foundcars=None,userfound=None,form=form)
            url=("http://127.0.0.1:5000/bookinghistory/"+request.form['search'])
            response=requests.get(url)
            bookinghistory=json.loads(response.text)
            if bookinghistory:
                return render_template("admin.html",title='Admin',unservicedcars=unservicedcars,servicehistory=servicehistory,cars=cars,users=users,user=username, rentalhistory=bookinghistory,foundcars=None,userfound=None,form=form)
        elif ('cardetails' in request.form):
            url=("http://127.0.0.1:5000/searchcar/"+request.form['carsearch'])
            response=requests.get(url)
            foundcars=json.loads(response.text)
            if foundcars:
                return render_template("admin.html",title='Admin',unservicedcars=unservicedcars,servicehistory=servicehistory,cars=cars,users=users,user=username,rentalhistory=None,foundcars=foundcars,userfound=None,form=form)
        elif('userdetails' in request.form):
            url=("http://127.0.0.1:5000/finduserdetails/"+request.form['usersearch'])
            response=requests.get(url)
            userfound=json.loads(response.text)
            if userfound!='Not Found':
                return render_template("admin.html",title='Admin',unservicedcars=unservicedcars,servicehistory=servicehistory,cars=cars,users=users,user=username,rentalhistory=None,foundcars=None,userfound=userfound,form=form)
            else:
                flash(f'User Not found, please try with another keyword','danger')
                return render_template("admin.html",title='Admin',unservicedcars=unservicedcars,servicehistory=servicehistory,cars=cars,users=users,user=username,rentalhistory=None,foundcars=None,userfound=None,form=form)
    return render_template("admin.html",title='Admin',unservicedcars=unservicedcars,servicehistory=servicehistory,cars=cars,users=users,user=username,form=form)

@site.route("/manager",methods=['GET','POST'])
def manager():
    url=("http://127.0.0.1:5000/username/"+session['email'])
    response=requests.get(url)
    username=json.loads(response.text)
    return render_template("manager.html",user=username,title="Manager")

@site.route("/engineer",methods=['GET', 'POST'])
def engineer():
    url=("http://127.0.0.1:5000/username/"+session['email'])
    response=requests.get(url)
    username=json.loads(response.text)
    url=("http://127.0.0.1:5000/findallocatedcars/"+session['email'])
    response=requests.get(url)
    availablecars=json.loads(response.text)
    url="http://127.0.0.1:5000/checkengineerdetails/"+session['email']
    response=requests.get(url)
    engineerdetails=json.loads(response.text)
    if engineerdetails=='No engineer found with that email':
        engineerdetails=session['email']
        needdetails=True
    else:
        needdetails=False
    print(needdetails)
    if request.method=="POST":
        if 'addengineerdetails' in request.form:
            url="http://127.0.0.1:5000/addengineerdetails"
            response=requests.post(url, json=request.form)
            response=json.loads(response.text)
            if 'Success' in response:
                flash(f'Details Added','success')
                return redirect(url_for('site.engineer'))
            else:
                flash(f'We have encountered an internal error, please try again later or contact the admin','danger')
                return redirect(url_for('site.engineer'))
    return render_template("engineer.html",title='Engineer',availablecars=availablecars,user=username,needdetails=needdetails,engineerdetails=engineerdetails, data=data)

@site.route("/logout",methods=['GET','POST'])
def logout():
    """
    Log out of webpage

    """
    session.clear()
    return redirect(url_for('site.login'))

@site.route("/booking",methods=['GET','POST'])
def booking():
    """
    Booking form from forms.py

    """
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
                    response=response.replace('"','')
                    response=response.replace('\n','')
                if response.__contains__("Vehicle Booked"):
                    flash(f'Booking Successful', 'success')
                    return redirect(url_for('site.home'))
                elif response.__contains__("Vehicl already"):
                    flash(f'Vehicle Is Unavailble for the requested time slot, please try another suitable time slot','danger')
                    return redirect(url_for('site.home'))
                else:
                    flash(f'Booking cannot be made, please try again later or with a different car/dates\nWe apologise for inconvenience caused','danger')
                    return redirect(url_for('site.home'))
        elif ('goback' in request.form):
            return redirect(url_for('site.home'))

    return render_template("booking.html",title='Booking Car',carid=None, username=session['email'],form=form)

@site.route("/modifyuser",methods=['GET','POST'])
def modifyuser():
    if request.method=='POST':
        if 'deleteuser' in request.form:
            url=("http://127.0.0.1:5000/deleteuser/"+request.form['emailtomodify'])
            response=requests.get(url)
            response=json.loads(response.text)
            if 'Success' in response:
                flash(f'User Has Been Deleted Successfully','success')
                return redirect(url_for('site.admin'))
            else:
                flash(f'Encountered an internal error while trying to delete user, please check logs for more information','danger')
                return redirect(url_for('site.admin'))
        if 'usermodify' in request.form:
            print("I am here")
            url=("http://127.0.0.1:5000/finduserdetails/"+request.form['emailtomodify'])
            response=requests.get(url)
            userdetails=json.loads(response.text)
            print(userdetails)
            return render_template("modifyuser.html",title="Modify User",userdetails=userdetails)
        if 'goback' in request.form:
            return redirect(url_for('site.admin'))            
        if 'modify' in request.form:
            if request.form['status']!='1' and request.form['status'] != '0':
                flash(f'Active Status can be either 0 or 1 only\nPlease try again!','danger')
                return redirect(url_for('site.admin'))
            url="http://127.0.0.1:5000/modifyuserdetails"
            response=requests.post(url,json=request.form)
            response=json.loads(response.text)
            if 'Success' in response:
                flash(f'User has been updated Successfully','success')
                return redirect(url_for('site.admin'))
    return render_template("modifyuser.html",title="Modify User")

@site.route("/modifycar",methods=['GET','POST'])
def modifycar():
    if request.method=='POST':
        if 'cartomodify' in request.form:
            url=("http://127.0.0.1:5000/findcardetails/"+request.form['cartomodify'])
            response=requests.get(url)
            cardetails=json.loads(response.text)
            return render_template("modifycar.html",cardetails=cardetails,title="Modify Car")
        if 'goback' in request.form:
            return redirect(url_for('site.admin'))
        if 'modify' in request.form:
            url="http://127.0.0.1:5000/modifycardetails"
            response=requests.post(url,json=request.form)
            response=json.loads(response.text)
            if 'Success' in response:
                flash(f'Car Details have been updated Successfully','success')
                return redirect(url_for('site.admin'))
    return render_template("modifycar.html",title="Modify Car")

@site.route("/about",methods=['GET','POST'])
def about():
    """
    About page

    """
    return render_template("about.html")

@site.route("/reportcar",methods=['GET','POST'])
def reportcar():
    if request.method=='POST':
        if 'goback' in request.form:
            return redirect(url_for('site.admin'))
        if 'cartoreport' in request.form:
            response=requests.get("http://127.0.0.1:5000/findengineers")
            engineers=json.loads(response.text)
            if engineers!='No Engineers Found':

                return render_template("reportcar.html",title='Report Car',engineerdetails=engineers,rego=request.form['cartoreport'])
            else:
                flash(f'No Engineers Found, Cannot Book Service','danger')
                return redirect(url_for('site.admin'))
        if 'report' in request.form:
            url="http://127.0.0.1:5000/createservicerequest"
            response=requests.post(url,json=request.form)
            response=response.text
            if response:
                    response=response.replace('"','')
                    response=response.replace('\n','')
                    if response.__contains__("Car Service Booked"):
                        flash(response,'success')
                        return redirect(url_for('site.admin'))
                    else:
                        flash(f'Service request could not be raised, please try again','danger')
                        return redirect(url_for('site.admin'))
    return render_template("reportcar.html",title='Report Car')

