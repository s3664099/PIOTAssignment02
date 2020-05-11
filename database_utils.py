import pymysql
import datetime
from pymysql.cursors import DictCursor
import gcalendar_utils as gcalendar

#A class for creating a connection to the database to enable manipulation
#and retrieval.
class databaseUtils:
	HOST = ""
	USER = ""
	PASSWORD = ""
	DATABASE = ""
	connection = None
	area_range = 0.0025
	service = None

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

		self.service = gcalendar.connect_calendar()

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
		#password=hash_password(password)
		with self.connection.cursor(DictCursor) as cur:
			response = "success"
			try:
				cur.execute("INSERT INTO user VALUES \
					('"+user_name+"','"+first_name+"','"+last_name+"','"+password+"','"+email+"')")
				self.connection.commit()
			except:
				response = "Email already used"
			self.connection.commit()
			return response

	#This method returns the password and the user name of the user
	def return_user(self, user_name):

		query = "SELECT username, password FROM user WHERE"

		return self.get_user(user_name, query)

	#Function that handles the return_user requests
	#Checks to see if the query is for a username, or for an email
	def get_user(self, user_name, query):

		with self.connection.cursor(DictCursor) as cur:
			results = cur.execute(query+" email='"+user_name+"'")
			
			if results == 0:
				cur.execute(query+" username='"+user_name+"'")

			return cur.fetchall()

	#Return user details
	def return_user_details(self, user_name):

		query = "SELECT * FROM user WHERE"

		return self.get_user(user_name, query)	

	#Gets a list of the bookings that the user has made
	def get_booking_history(self, email):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM booking WHERE email='"+email+"'")

			return cur.fetchall()

	#Returns the details of a particular vehicle
	def return_vehicle_details(self, search):
		car="Not Found"
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
				colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
				AND m.bodytype = b.bodytype AND (c.rego='"+search+"' OR c.make='"+search+"' OR c.model='"+search+"' \
				OR c.colour='"+search+"' OR b.bodytype='"+search+"' OR  seats='"+search+"') ")

			cars = cur.fetchall()
			if cars:
				return cars
			return car

	def return_vehicle_details_location(self, lng, lat, search):

		cars = self.return_vehicle_details(search)
		cars = self.filter_location(lng, lat, cars)

		return cars

	#Takes the details of the users location and returns all nearby cars and returns ones that aren't currently booked
	def filter_location(self, lng, lat, cars):

		#Variables to be used. The range is arbitrary and can be changed
		top_long = lng + databaseUtils.area_range
		bottom_long = lng - databaseUtils.area_range
		left_lat = lat - databaseUtils.area_range
		right_lat = lat + databaseUtils.area_range
		vehicle_list = []

		for car in cars:
			if car["locationlong"] < top_long and car["locationlong"] > bottom_long and car["locationlat"] > left_lat and car["locationlat"] < right_lat:
				vehicle_list.append(car)
				vehicle_list = self.sort_cars(vehicle_list)

		return vehicle_list

	#Takes the details of the users location and returns all nearby cars and returns ones that aren't currently booked
	def get_available_cars(self, lng, lat):

		cars = self.get_all_cars()

		vehicle_list = self.filter_location(lng, lat, cars)
		vehicle_list = self.sort_cars(vehicle_list)

		return vehicle_list

	#Function designed to sort the cars based of whether they have been booked or not
	def sort_cars(self, vehicle_list):

		with self.connection.cursor(DictCursor) as cur:

			temp_vehicle_list = []
			unbooked_vehicle_list = []

			#checks each of the vehicles returned to see if they have been booked
			for car in vehicle_list:
				temp_vehicle_list.append(car)

			for car in temp_vehicle_list:

				car_booked = False

				#Gets a list of bookings based on that vehicle
				cur.execute("SELECT pickuptime, dropofftime, status FROM booking WHERE rego = '"+car['rego']+"'")
				car_booking = cur.fetchall()

				if car_booking:

					for booking in car_booking:

						#Checks to see if the car has been booked in the current period
						#If so, sets the flag to true so that the vehicle is not returned
						if datetime.datetime.now() > booking['pickuptime'] and datetime.datetime.now() < booking['dropofftime']:

							if (booking['status'] == 'BOOKED') or (booking['status'] == 'ACTIVE'):
								car_booked = True

				if car_booked == False:
					unbooked_vehicle_list.append(car)

			return unbooked_vehicle_list


	def get_all_cars(self):
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT rego, make, model, locationlat, locationlong FROM car")

			vehicle_list = self.sort_cars(cur.fetchall())

		return vehicle_list

	#Function to book a vehicle and adds booking to the database
	def book_vehicle(self, name, rego, pickup, dropoff):
		with self.connection.cursor(DictCursor) as cur:

			#gets booking history for vehicle
			cur.execute("SELECT pickuptime, dropofftime, status FROM booking WHERE rego = '"+rego+"'")

			#Iterates through booking history
			for bookings in cur.fetchall():
				#checks to see if booking date overlaps
				if (pickup > bookings['pickuptime'] and pickup < bookings['dropofftime']) or (
					dropoff > bookings['pickuptime'] and dropoff < bookings['dropofftime']):

					if (bookings['status'] == 'BOOKED') or (bookings['status'] == 'ACTIVE'):

						#if it does returns invalid booking
						return "Vehicle already booked"

			#The hourly price for that particular car is retrieved form the database
			cur.execute("SELECT hourlyPrice FROM bodytype JOIN makemodel on makemodel.bodytype = bodytype.bodytype\
						JOIN car ON car.model = makemodel.model WHERE rego = '"+rego+"'")

			#Source: https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
			#Calculates the total cost of the booking
			price = cur.fetchall().pop()
			price = float(price['hourlyPrice'])
			booking_time = dropoff - pickup
#			print("\n\n\n Booking Time ")
#			print(booking_time)
#			print("\n\n")
			booking_time = divmod(booking_time.total_seconds(), 3600)[0]

			#Source: https://kite.com/python/answers/how-to-print-a-float-with-two-decimal-places-in-python
			total_cost = price*booking_time
			total_cost = "{:.2f}".format(total_cost)

			cur.execute("SELECT make, model FROM car WHERE rego = '"+rego+"'")
			car_type = cur.fetchall().pop()

			googleId = gcalendar.insert(pickup.isoformat() +"Z", dropoff.isoformat() +"Z", rego, car_type['make'], 
										car_type['model'], total_cost, self.service)

			#The booking is added to the database and the results returned to the user
			cur.execute("INSERT INTO booking (rego, email, pickuptime, dropofftime, totalcost, status, googleEventId) \
						VALUES ('"+rego+"', '"+name+"', '"+str(pickup)+"','"+str(dropoff)+"',"+total_cost+", 'BOOKED','"+googleId+"')")
			self.connection.commit()
			cur.execute("SELECT LAST_INSERT_ID()")
			insert_id = cur.fetchall().pop()

			return "Vehicle Booked, your booking number is "+str(insert_id['LAST_INSERT_ID()'])+" and the price is $"+total_cost

	def cancel_booking(self, name, booking_number):

		with self.connection.cursor(DictCursor) as cur:

			#gets the booking based on the booking number
			row_count = cur.execute("SELECT email, pickuptime, dropofftime, status, googleEventId FROM booking WHERE \
									bookingnumber = '"+str(booking_number)+"'")

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

				gcalendar.remove_event(results['googleEventId'], self.service)

				#If they do, the booking is cancelled and the entry cleared
				cur.execute("UPDATE booking SET status = 'CANCELLED' WHERE bookingnumber = '"+str(booking_number)+"'")
				return "Booking successfully cancelled"
				self.connection.commit()
				

				


				









