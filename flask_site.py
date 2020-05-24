"""
.. module:: flask_site

"""
from datetime import datetime
from google.cloud import storage
import json,os,requests, shutil
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Blueprint, request, render_template, session, flash, url_for, redirect
from forms import RegistrationForm, LoginForm, BookingForm
from Encoding.encode_recognise import recognise
from config import app

site = Blueprint("site", __name__)
ALLOWED_EXTENSIONS = {'png'}


def download_blob():
        """
        Downloads a blob from the bucket.
        
        """
        bucket_name = "car-hire"
        source_blob_name = "encodings.pickle"
        destination_file_name = "Encoding/encodings.pickle"

        storage_client = storage.Client() 
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)


def allowed_file(filename):
    """
    Allowed files

    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return render_template("about.html")
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file','danger')
                return redirect(url_for("site.register"))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
                img=os.path.join("Images/",filename)
                download_blob()
                exists=recognise("Encoding/encodings.pickle",img)
                if exists!="Unknown":
                    flash(f'User image already exists, please create a new user','danger')
                    return redirect(url_for('site.register'))
                else:
                    result=json.dumps(request.form)
                    result=json.loads(result)
                    url=("http://127.0.0.1:5000/registeruser")
                    response=requests.post(url,json=result)
                    response=response.text
                    if response:
                        response=response.replace('"','')
                        response=response.replace('\n','')
                    if response.__contains__("success"):
                        dir=os.path.join("Encoding/dataset/",request.form['email'])
                        os.mkdir(dir)
                        shutil.copy(img,os.path.abspath(dir))
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

@site.route("/about",methods=['GET','POST'])
def about():
    """
    About page

    """
    return render_template("about.html")
