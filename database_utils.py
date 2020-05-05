import pymysql
import datetime
from pymysql.cursors import DictCursor

#A class for creating a connection to the database to enable manipulation
#and retrieval.
class databaseUtils:
	HOST = ""
	USER = ""
	PASSWORD = ""
	DATABASE = ""
	connection = None
	area_range = 0.0025

	#Establishes the connection by passing through the required variables
	#The variables aren't hardcoded to enable testing on a test database
	def __init__ (self, host, user, password, database):
		databaseUtils.HOST = host
		databaseUtils.USER = user
		databaseUtils.PASSWORD = password
		databaseUtils.DATABASE = database

		#This is where the connection is made, and saved as a variable in the class
		if databaseUtils.connection == None:
			myConnection = pymysql.connect(host=databaseUtils.HOST, user = databaseUtils.USER, passwd = databaseUtils.PASSWORD, 
    			db = databaseUtils.DATABASE, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.connection = myConnection

	#The following methods are for closing the database
	def close_connection(self):

		self.connection.close()

	def __enter__ (self):
		return self

	def __exit__(self, type, value, traceback):
		self.close_connection()

	#This returns the connection to the database to enable a connection elsewhere
	def get_connection(self):
		return self.connection

	#This method is designed to insert a new user into the database
	def insert_user(self, user_name, first_name, last_name, password, email):
		with self.connection.cursor(DictCursor) as cur:
			response = "success"
			try:
				cur.execute("INSERT INTO user VALUES \
					('"+user_name+"','"+first_name+"','"+last_name+"','"+password+"','"+email+"')")
			except:
				response = "Email already used"
			self.connection.commit()
			return response

	#This method returns the password and the user name of the user
	def return_user(self, user_name):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT username, password FROM user WHERE email='"+user_name+"'")
			return cur.fetchall()

	#Return user details
	def return_user_details(self, user_name):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM user WHERE email='"+user_name+"'")

			return cur.fetchall()	

	#Gets a list of the bookings that the user has made
	def get_booking_history(self, user_name):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM booking WHERE username='"+user_name+"'")

			return cur.fetchall()

	#Returns the details of a particular vehicle
	def return_vehicle_details(self, search):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
				colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
				AND m.bodytype = b.bodytype AND c.rego='"+search+"'")

			cars = cur.fetchall()
			if cars:
				return cars
			else:
				cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
				colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
				AND m.bodytype = b.bodytype AND c.make='"+search+"'")

				cars = cur.fetchall()
				if cars:
					return cars
				else:
					cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
					colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
					AND m.bodytype = b.bodytype AND c.model='"+search+"'")

					cars = cur.fetchall()
					if cars:
						return cars
					else:
						cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
						colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
						AND m.bodytype = b.bodytype AND c.colour='"+search+"'")

						cars = cur.fetchall()
						if cars:
							return cars
						else:
							cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
							colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
							AND m.bodytype = b.bodytype AND b.bodytype='"+search+"'")

							cars = cur.fetchall()
							if cars:
								return cars
							else:
								cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
								colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
								AND m.bodytype = b.bodytype AND c.seats='"+search+"'")

								cars = cur.fetchall()
								if cars:
									return cars



	#Takes the details of the users location and returns all nearby cars and returns ones that aren't currently booked
	def get_available_cars(self, lng, lat):

		#Variables to be used. The range is arbitrary and can be changed
		top_long = str(lng + databaseUtils.area_range)
		bottom_long = str(lng - databaseUtils.area_range)
		left_lat = str(lat - databaseUtils.area_range)
		right_lat = str(lat + databaseUtils.area_range)
		vehicle_list = []

		#Get a list of vehicles based on area which has been passed through
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT rego, make, model, locationlong, locationlat FROM car \
				WHERE locationlong<"+top_long+" and locationlong > "+bottom_long+" and \
				locationlat > "+left_lat+" and locationlat<"+right_lat)

			vehicle_list = self.sort_cars(cur.fetchall(), cur)

		return vehicle_list

	def sort_cars(self, vehicle_list, cur):

		temp_vehicle_list = []
		unbooked_vehicle_list = []

		#checks each of the vehicles returned to see if they have been booked
		for car in vehicle_list:
			temp_vehicle_list.append(car)

		for car in temp_vehicle_list:

			car_booked = False

			#Gets a list of bookings based on that vehicle
			cur.execute("SELECT pickuptime, dropofftime FROM booking WHERE rego = '"+car['rego']+"'")
			car_booking = cur.fetchall()

			if car_booking:

				for booking in car_booking:

					#Checks to see if the car has been booked in the current period
					#If so, sets the flag to true so that the vehicle is not returned
					if datetime.datetime.now() > booking['pickuptime'] and datetime.datetime.now() < booking['dropofftime']:
						car_booked = True

			if car_booked == False:
				unbooked_vehicle_list.append(car)

		#print(len(unbooked_vehicle_list))

		return unbooked_vehicle_list


	def get_all_cars(self):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT rego, make, model FROM car")

			vehicle_list = self.sort_cars(cur.fetchall(), cur)

		return vehicle_list

	#Function to book a vehicle and adds booking to the database
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

	def cancel_booking(self, name, booking_number):

		with self.connection.cursor(DictCursor) as cur:

			#gets the booking based on the booking number
			row_count = cur.execute("SELECT email, pickuptime, dropofftime, active FROM booking WHERE bookingnumber\
									 = '"+str(booking_number)+"'")

			#Checks to see if the booking exists
			if row_count == 0:
				return "No booking exists"

			results = cur.fetchall().pop()
			username = results['email']
			pickup = results['pickuptime']
			dropoff = results['dropofftime']

			time = datetime.datetime.now()

			#Checks to see if the booking is a valud booking to be cancelled	
			if name != username:
				return "Can't cancel somebody else's booking"
			elif time > dropoff:
				return "Can't cancel a previous booking"
			elif time > pickup:
				return "Can't cancel a booking in progress"
			else:

				#If they do, the booking is cancelled and the entry cleared
				cur.execute("UPDATE booking SET active = 0 WHERE bookingnumber = '"+str(booking_number)+"'")
				return "Booking successfully cancelled"
				

				


				









