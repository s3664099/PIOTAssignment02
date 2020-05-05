
from flask import Flask, Blueprint, request, jsonify, render_template, session, flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app
from flask_api import myConnection
from forms import BookingForm
from login import new_user, logon, verify_register, verify_password
from databaseSetup import user, booking
import os, requests, json

booking = Blueprint('booking_blueprint',__name__)

def book_vehicle(self, name, rego, pickup, dropoff):
    
		with self.connection.cursor(DictCursor) as cur:

			#gets booking history for vehicle
			cur.execute("SELECT pickuptime, dropofftime, active FROM booking WHERE rego = '"+rego+"'")

			#Iterates through booking history
			for bookings in cur.fetchall():

				#checks to see if booking date overlaps
				if (pickup > bookings['pickuptime'] and pickup < bookings['dropofftime'] and bookings['active'] == 1) or (
					dropoff > bookings['pickuptime'] and dropoff < bookings['dropofftime'] and bookings['active'] == 1):

					#if it does returns invalid booking
					return "Vehicle already booked"

			#The hourly price for that particular car is retrieved form the database
			cur.execute("SELECT hourlyPrice FROM bodytype JOIN makemodel on makemodel.bodytype = bodytype.bodytype\
						JOIN car ON car.model = makemodel.model\
						WHERE rego = '"+rego+"'")

			#Source: https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
			#Calculates the total cost of the booking
			price = cur.fetchall().pop()
			price = float(price['hourlyPrice'])
			booking_time = dropoff - pickup
			booking_time = divmod(booking_time.total_seconds(), 3600)[0]

			#Source: https://kite.com/python/answers/how-to-print-a-float-with-two-decimal-places-in-python
			total_cost = price*booking_time
			total_cost = "{:.2f}".format(total_cost)

			#The booking is added to the database and the results returned to the user
			cur.execute("INSERT INTO booking (rego, email, pickuptime, dropofftime, totalcost, active) \
						VALUES ('"+rego+"', '"+name+"', '"+str(pickup)+"','"+str(dropoff)+"',"+total_cost+", 1)")
			cur.execute("SELECT LAST_INSERT_ID()")
			insert_id = cur.fetchall().pop()

			return "Vehicle Booked, your booking number is "+str(insert_id['LAST_INSERT_ID()'])+" and the price is $"+total_cost

@booking.route('/bookings', methods=('GET', 'POST'))
def new_booking():
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

    form = BookingForm()
    if form.validate_on_submit():
        print (form.car_id.data)
        booking = Booking(bookingnumber=form.bookingnumber.data,
                    rego=form.rego.data,
                    email=form.email.data,
                    pickuptime=form.pickuptime.data,
                    dropofftime=form.dropofftime.data
                    totalcost=form.totalcost.data
                    )
        booking_validation = booking.is_car_avaiable()
        if booking_validation['result'] == False:
            flash(booking_validation['reason'])
            return render_template('booking.html', title='Bookings', form=form)
        db.session.add(booking)
        db.session.commit()
        flash('Thanks for making a booking')
        return render_template('booking.html', title='Bookings',form=form)
