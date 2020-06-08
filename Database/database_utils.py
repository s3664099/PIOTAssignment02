"""
.. module:: database_utils

"""
import pymysql
import datetime
from pymysql.cursors import DictCursor
#import Database.gcalendar_utils as gcalendar

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
		"""
		Database varriables

		"""
		databaseUtils.HOST = host
		databaseUtils.USER = user
		databaseUtils.PASSWORD = password
		databaseUtils.DATABASE = database

		#This is where the connection is made, and saved as a variable in the class
		if databaseUtils.connection == None:
			myConnection = pymysql.connect(host=databaseUtils.HOST, user = databaseUtils.USER, passwd = databaseUtils.PASSWORD, 
    			db = databaseUtils.DATABASE, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.connection = myConnection

		#self.service = gcalendar.connect_calendar()

	#The following methods are for closing the database
	def close_connection(self):
		"""
		Closing the connection of the database

		"""
		self.connection.close()

	def __enter__ (self):
		"""
		Enter

		"""
		return self

	def __exit__(self, type, value, traceback):
		"""
		Exit

		"""
		self.close_connection()

	#This returns the connection to the database to enable a connection elsewhere
	def get_connection(self):
		"""
		Enable connection

		"""
		return self.connection

	#This method is designed to insert a new user into the database
	def insert_user(self, user_name, first_name, last_name, password, email):
		"""
		Insert new user details

		"""

		with self.connection.cursor(DictCursor) as cur:
			response = "success"
			try:
				cur.execute("INSERT INTO user VALUES \
					('{}','{}','{}','{}','{}')".format(user_name, first_name, last_name, password, email))
				self.connection.commit()
			except:
				response = "Email already used"
			self.connection.commit()
			return response

	#These three methods below work to return user details, one for everything
	#About the user, and the othe ronly the username/email and password
	#The third, middle, function actually handles the user requests
	def return_user(self, user_name):
		"""
		Fetch user details for everything

		"""

		query = "SELECT username, password FROM user WHERE"

		return self.get_user(user_name, query)

	def get_user(self, user_name, query):
		"""
		Fetch user details for username/email and password

		"""

		with self.connection.cursor(DictCursor) as cur:
			results = cur.execute("{} email='{}'".format(query,user_name))
			
			if results == 0:
				cur.execute("{} username='{}'".format(query,user_name))

			return cur.fetchall()

	def return_user_details(self, user_name):
		"""
		Handle user requests

		"""

		query = "SELECT * FROM user WHERE"

		return self.get_user(user_name, query)	

	#Gets a list of the bookings that the user has made
	def get_booking_history(self, email):
		"""
		List of bookings that users made

		"""
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM booking WHERE email='{}'".format(email))

			return cur.fetchall()

	#The following three methods 
	#Gets confirmed booking for a user for a particular car, active books, bookings within a particular time
	#TODO: Try to merge them to help with code quality
	def get_confirmed_booking_for_user(self,email,rego,time):
		"""
		Confirmed booking for user

		"""

		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM booking where email='{}' and status='BOOKED' and rego='{}' and \
						(pickuptime <='{}' and dropofftime>='{}')".format(email, rego, time, time))

			return cur.fetchall()

	#Gets Active booking for a user for a particular car
	def get_active_booking_for_user(self,email,rego):
		"""
		Active booking

		"""

		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM booking where email='{}' and status='ACTIVE' and rego='{}'".format(email, rego))

			return cur.fetchall()
			
	#Gets confirmed bookings for a user
	def get_confirmed_bookings(self,email):
		"""
		Confirmed bookings

		"""
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT * FROM booking where email='{}' and status='BOOKED'".format(email))

			return cur.fetchall()

	#Returns the details of a particular vehicle, the query is structured to search by
	#specific values for the vehicle
	def return_vehicle_details(self, search):
		"""
		Details of a particular vehicle

		"""
		car="Not Found"
		with self.connection.cursor(DictCursor) as cur:
			cur.execute("SELECT rego, c.make, c.model, locationlong, locationlat, colour, b.bodytype, seats, hourlyPrice \
				colour FROM car c, bodytype b, makemodel m WHERE c.model = m.model \
				AND m.bodytype = b.bodytype AND c.available = 1 AND (c.rego='{}' OR c.make='{}' OR c.model='{}' \
				OR c.colour='{}' OR b.bodytype='{}' OR  seats='{}') ".format(search, search, search, search, search, search))

			cars = cur.fetchall()
			if cars:
				return cars
			return car

	#This method returns vehicles in a specified loations based on specific parameters
	def return_vehicle_details_location(self, lng, lat, search):
		"""
		Details of vehicles in a specified locations

		"""

		cars = self.return_vehicle_details(search)
		cars = self.filter_location(lng, lat, cars)

		return cars

	#Takes the details of the users location and returns all nearby cars and returns ones that aren't currently booked
	def filter_location(self, lng, lat, cars):
		"""
		Details of users location and nearby cars that aren't booked

		"""

		#Variables to be used. The range is arbitrary and can be changed
		top_long = lng + databaseUtils.area_range
		bottom_long = lng - databaseUtils.area_range
		left_lat = lat - databaseUtils.area_range
		right_lat = lat + databaseUtils.area_range
		vehicle_list = []

		for car in cars:
			if car["locationlong"] < top_long and car["locationlong"] > bottom_long and car["locationlat"] > left_lat and car["locationlat"] < right_lat:
				vehicle_list.append(car)

		return vehicle_list

	#Takes the details of the users location and returns all nearby cars and returns ones that aren't currently booked
	def get_available_cars(self, lng, lat):
		"""
		Get all available cars

		"""
		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT rego, make, model, locationlat, locationlong FROM car WHERE available = '1'")

			cars = cur.fetchall()

			vehicle_list = self.filter_location(lng, lat, cars)

			return vehicle_list

	#Changes the availability status of the vehicle
	def update_availability(self, rego, available):
		"""
		Update availability status of the vehicles

		"""
		with self.connection.cursor(DictCursor) as cur:
			try:
				cur.execute("UPDATE car SET available = {} WHERE rego = '{}' and available!='\
					{}'".format(available, rego, available))
			except pymysql.Error as e:
					print("Caught error %d: %s" % (e.args[0], e.args[1]))
					return "Error"
			self.connection.commit()
			return "Success"

	#Returns the availability status of the vehicle
	def get_availability(self, rego):
		"""
		Get availability status

		""" 
		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT available FROM car WHERE rego = '{}'".format(rego))	

			return cur.fetchall()	

	def get_all_cars(self):
		"""
		All cars

		"""
		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT rego, make, model, colour, locationlat, locationlong FROM car WHERE available ='1'")

			vehicle_list = cur.fetchall()

		return vehicle_list

	#Function to book a vehicle and adds booking to the database
	def book_vehicle(self, name, rego, pickup, dropoff):
		"""
		Book vehicle

		"""
		with self.connection.cursor(DictCursor) as cur:

			#gets booking history for vehicle
			cur.execute("SELECT pickuptime, dropofftime, status FROM booking WHERE rego = '{}'".format(rego))

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
						JOIN car ON car.model = makemodel.model WHERE rego = '{}'".format(rego))

			#Source: https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
			#Calculates the total cost of the booking
			price = cur.fetchall().pop()
			price = float(price['hourlyPrice'])
			booking_time = dropoff - pickup

			booking_time = divmod(booking_time.total_seconds(), 3600)[0]

			#Source: https://kite.com/python/answers/how-to-print-a-float-with-two-decimal-places-in-python
			total_cost = price*(booking_time+1)
			total_cost = "{:.2f}".format(total_cost)

			cur.execute("SELECT make, model FROM car WHERE rego = '{}'".format(rego))
			car_type = cur.fetchall().pop()
			googleId="None"
			try:
				googleId = gcalendar.insert(pickup.isoformat() +"Z", dropoff.isoformat() +"Z", rego, car_type['make'], 
										car_type['model'], total_cost, name, self.service)
			except:
				print("unable to update calendar")

			#The booking is added to the database and the results returned to the user
			try:
				cur.execute("INSERT INTO booking (rego, email, pickuptime, dropofftime, totalcost, status, googleEventId) \
						VALUES ('{}', '{}', '{}','{}',{}, 'BOOKED','{}')\
						".format(rego, name, pickup, dropoff, total_cost, googleId))
			except pymysql.Error as e:
				print("Caught error %d: %s" % (e.args[0], e.args[1]))
				return "Error"
			self.connection.commit()
			cur.execute("SELECT LAST_INSERT_ID()")
			insert_id = cur.fetchall().pop()

			return "Vehicle Booked, your booking number is {} and the price is ${}".format(insert_id['LAST_INSERT_ID()'], total_cost)

	#This method is used to cancel a booking for the vehicle.
	def cancel_booking(self, name, booking_number):
		"""
		Cancel booking of the vehicle

		"""

		with self.connection.cursor(DictCursor) as cur:

			#gets the booking based on the booking number
			row_count = cur.execute("SELECT email, pickuptime, dropofftime, status, googleEventId FROM booking WHERE \
									bookingnumber = '{}'".format(booking_number))

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

				try:
					gcalendar.remove_event(results['googleEventId'], self.service)
				except:
					print("Unable to update calendar")

				try:

					#If they do, the booking is cancelled and the entry cleared
					cur.execute("UPDATE booking SET status = 'CANCELLED' WHERE bookingnumber = '{}'".format(booking_number))
				except pymysql.Error as e:
					print("Caught error %d: %s" % (e.args[0], e.args[1]))
					return "Error"
				self.connection.commit()
				return "Booking successfully cancelled"
				

	#Returns the booking status of the vehicle. For testing purposes
	def get_booking_status(self, booking_number):
		"""
		Booking status

		"""

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT status FROM booking WHERE bookingnumber = '{}'".format(booking_number))

			return cur.fetchall()

	#Updates the booking status of the booking.
	def change_booking_status(self, booking_number, status):
		"""
		Change booking status

		"""

		with self.connection.cursor(DictCursor) as cur:
			try:
				cur.execute("UPDATE booking SET status = '{}' WHERE bookingnumber = '{}'".format(status, booking_number))
			except pymysql.Error as e:
					print("Caught error %d: %s" % (e.args[0], e.args[1]))
					return "Error"
			self.connection.commit()
			return "Success"

	#This method is designed to create an employee.
	def create_employee(self, user_name, first_name, last_name, password, email, role):
		#Commenting the role validation as this is not a user input. Default values are passed for the user to select on the form during registeration
		"""if role != 'MANAGER':
			if role != 'ADMIN':
				if role != 'ENGINEER':
					return 'invalid role'
		"""
		with self.connection.cursor(DictCursor) as cur:
			response = "success"
			#Registeration form accepts user's email and user name as this will be needed for appropriate pushbullet messaging
			"""email = "{}.{}@carshare.com".format(first_name[0], last_name[0])
			user_name = "{}{}".format(first_name,last_name)
			"""
			try:
				cur.execute("INSERT INTO user VALUES \
					('{}','{}','{}','{}','{}')".format(user_name, first_name, last_name, password, email))
				cur.execute("INSERT INTO user_role VALUES ('{}','{}',0,'{}')".format(email, 1, role))
				self.connection.commit()
			#for sql try and catch blocks, please throw the sql exception as it is required for debugging issues and better code maintanence
			except pymysql.Error as e:
				print(e)
				response='Email already used'

			self.connection.commit()
			return response

	#Methods to return employees
	def return_employee(self, email):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT * FROM user, user_role WHERE user.email = user_role.email and user.email = '{}'".format(email))

			return cur.fetchall()

	def return_employee_type(self, role):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT * FROM user, user_role WHERE user.email = user_role.email and user_role.role = '{}'".format(role))

			return cur.fetchall()

	def return_all_employees(self):

		with self.connection.cursor(DictCursor) as cur:		

			cur.execute("SELECT * FROM user, user_role WHERE user.email = user_role.email and (user_role.role = 'ENGINEER' or \
				user_role.role = \'ADMIN' or user_role.role = 'MANAGER')")

			return cur.fetchall()
			
	#Activate Employee
	def activate_employee(self, email):


		with self.connection.cursor(DictCursor) as cur:

			response = "success"

			if cur.execute("SELECT * FROM user_role WHERE email = '{}'".format(email)):
				cur.execute("UPDATE user_role SET is_active = 1 WHERE email = '{}'".format(email))
				self.connection.commit()
			else:
				response = "user not found"							

			return response

	def add_engineer(self, email, mac_address, token):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("INSERT INTO engineer VALUES ('{}','{}','{}')".format(email, mac_address,token))

			self.connection.commit()

	def get_engineer(self, email):

		with self.connection.cursor(DictCursor) as cur:

			results = cur.execute("SELECT * FROM engineer WHERE email = '{}'".format(email))

			if results:
				return cur.fetchall()
			else:
				return "No engineer found with that email"

	def get_mac_address(self, email):

		with self.connection.cursor(DictCursor) as cur:	

			results = cur.execute("SELECT mac_address FROM engineer WHERE email = '{}'".format(email))

			if results:

				return cur.fetchall()

			else:

				return "No engineer found with that email"

	def get_token(self, email):

		with self.connection.cursor(DictCursor) as cur:	

			results = cur.execute("SELECT pb_token FROM engineer WHERE email = '{}'".format(email))

			if results:

				return cur.fetchall()

			else:

				return "No engineer found with that email"		


	def get_all_mac_addresses(self):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT mac_address FROM engineer")

			return cur.fetchall()

	#Create Service Request
	def create_service_request(self, rego, post_code, email):

		with self.connection.cursor(DictCursor) as cur:

			result = "car booked for service"	

			try:
				if cur.execute("SELECT * FROM car WHERE rego = '{}'".format(rego)):

					if cur.execute("SELECT * FROM user_role WHERE email = '{}'".format(email)):

						if cur.execute("SELECT * FROM car_service WHERE rego = '{}' AND needs_service = 1".format(rego)):

							return 'A service request has already been booked for vehicle {}'.format(rego)

						else:

							cur.execute("INSERT INTO car_service (rego, email, needs_service, engineer_assigned, post_code) VALUES \
										('{}','{}',1,0,'{}')".format(rego, email, post_code))
							cur.execute("UPDATE car SET available = 0 WHERE rego = '{}'".format(rego))

							self.connection.commit()

							cur.execute("SELECT LAST_INSERT_ID()")
							service_id = cur.fetchall().pop()

							result += '. The service number is {}'.format(service_id['LAST_INSERT_ID()'])
					else:
						return "Invalid email. Unable to book vehicle for service"
				else:
					return "Unable to book vehicle for service, no such vehicle exists"

			except pymysql.Error as e:
				print(e)

			return result


	def get_service_request(self, service_id):

		with self.connection.cursor(DictCursor) as cur:

			if cur.execute("SELECT * FROM car_service WHERE request_no = '{}'".format(service_id)):
				return cur.fetchall()
			else:
				return "No service request found with id {}".format(service_id)

	def get_all_service_requests(self):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT * FROM car_service")

			return cur.fetchall()

	def get_all_active_service_requests(self):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT * FROM car_service WHERE needs_service = 1")

			return cur.fetchall()

	def get_all_unassigned_service_requests(self):

		with self.connection.cursor(DictCursor) as cur:

			cur.execute("SELECT * FROM car_service WHERE engineer_assigned = 0")

			return cur.fetchall()

	def assign_engineer(self, email, service_id):

		with self.connection.cursor(DictCursor) as cur:

			try:

				service_request = self.get_service_request(service_id)

				if service_request == "No service request found with id {}".format(service_id):
					return service_request
				else:
					service_request = service_request.pop()
					if service_request["engineer_assigned"] == 1:
						return "engineer already assigned to this service request"
					elif service_request["needs_service"] == 0:
						return "This service request is not active"
					elif self.get_engineer(email) != "No engineer found with that email":
						cur.execute("UPDATE car_service SET engineer_assigned = 1, email = '{}' WHERE request_no = '{}'".format(email, service_id))
						return "Engineer successfully assigned"
					else:
						return "No engineer found with email {}".format(email)
			except pymysql.Error as e:
				print(e)

				return "Unable to assign engineer"

	def service_complete(self, service_id):

		with self.connection.cursor(DictCursor) as cur:

			try:
				service_request = self.get_service_request(service_id)

				if service_request == "No service request found with id {}".format(service_id):
					return service_request
				else:
					service_request = service_request.pop()

					if service_request["engineer_assigned"] == 0:
						return "No engineer assigned to this service request"
					elif service_request["needs_service"] == 0:
						return "Service request not active"
					else:
						cur.execute("UPDATE car_service SET needs_service = 0 WHERE request_no = '{}'".format(service_id))
						return "Service completed"
			except:
				return "Unable to update service"

