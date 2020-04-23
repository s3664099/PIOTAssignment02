import pymysql
import datetime

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
    			db = databaseUtils.DATABASE, charset='utf8')
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
		with self.connection.cursor() as cur:
			response = "success"
			try:
				cur.execute("INSERT INTO user VALUES ('"+user_name+"','"+first_name+"','"+last_name+"','"+password+"','"+email+"')")
			except:
				response = "User name already used"
			self.connection.commit()
			return response

	#This method returns the password and the user name of the user
	def return_user(self, user_name):
		with self.connection.cursor() as cur:
			cur.execute("SELECT username, password FROM user WHERE username='"+user_name+"'")
			return cur.fetchall()

	#Return user details
	def return_user_details(self, user_name):
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM user WHERE username='"+user_name+"'")

			return cur.fetchall()	

	#Gets a list of the bookings that the user has made
	def get_booking_history(self, user_name):
		with self.connection.cursor() as cur:
			cur.execute("SELECT rego, pickuptime, dropofftime, totalcost FROM booking WHERE username='"+user_name+"'")

			return cur.fetchall()

	#Returns the details of a particular vehicle
	def return_vehicle_details(self, rego):
		with self.connection.cursor() as cur:
			cur.execute("SELECT rego, make, model, locationlong, locationlat, colour FROM car WHERE rego='"+rego+"'")

			#Need to also return body type, seats and hourly price
			#Place details into a map
			#With make and model, get bodytype, seats, and hourly price

			return cur.fetchall()

	#Takes the details of the users location and returns all nearby cars and returns ones that aren't currently booked
	def get_available_cars(self, lng, lat):

		#Variables to be used. The range is arbitrary and can be changed
		top_long = str(lng + databaseUtils.area_range)
		bottom_long = str(lng - databaseUtils.area_range)
		left_lat = str(lat - databaseUtils.area_range)
		right_lat = str(lat + databaseUtils.area_range)
		temp_vehicle_list = []
		vehicle_list = []

		#Get a list of vehicles based on area which has been passed through
		with self.connection.cursor() as cur:
			cur.execute("SELECT rego, make, model, locationlong, locationlat FROM car WHERE locationlong<"+top_long+" and locationlong > "+bottom_long+" and locationlat > "+left_lat+" and locationlat<"+right_lat)

			#checks each of the vehicles returned to see if they have been booked
			for car in cur.fetchall():
				temp_vehicle_list.append(car)

			for car in temp_vehicle_list:

				car_booked = False

				#Gets a list of bookings based on that vehicle
				cur.execute("SELECT pickuptime, dropofftime FROM booking WHERE rego = '"+car[0]+"'")
				car_booking = cur.fetchall()

				if car_booking:

					for booking in car_booking:

						#Checks to see if the car has been booked in the current period
						#If so, sets the flag to true so that the vehicle is not returned
						if datetime.datetime.now() > booking[0] and datetime.datetime.now() < booking[1]:
							car_booked = True

				if car_booked == False:
					vehicle_list.append(car)

		return vehicle_list

		def book_vehicle(self, name, rego, pickup, dropoff):

			with self.connection.cursor() as cur:

				#gets booking history for vehicle
				cur.execute("SELECT pickuptime, dropofftime FROM booking WHERE rego = '"+rego+"'")

				#Iterates through booking history
				for bookings in cur.fetchall():

					#checks to see if booking date overlaps
					if (pickup > bookings.pickuptime and pickup < bookings.dropofftime) or (
						dropoff > bookings.pickuptime and dropoff < bookings.dropofftime):

						#if it does returns invalid booking
						return "Vehicle alredy booked"

					else:

						#Calculate number of hours booked and get fee based on bodytype
						#Create function to calculate hourly price
							#Takes pickup/dropoff and price, returns total price
						

						cur.execute("INSERT INTO booking (rego, username, pickuptime, dropofftime, totalcost) VALUES ('"+rego+"', '"+name+"', '"+str(pickup)+"','"+str(dropoff)+"',42.00)")









			
			
			#if it doesn't returns successful booking, and booking number


		def cancel_booking(self, name, booking_number):

			with self.connection.cursor() as cur:

				#gets the booking based on the booking number
				cur.execute("SELECT username FROM booking WHERE bookingnumber = '"+booking_number+"'")

			#confirms that the names match
			#If they do, the booking is cancelled and the entry cleared
			#If they don't, an error is returned

				









