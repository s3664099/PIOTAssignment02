import unittest
#import pymysql
import db_singleton as singleton
import database_utils as database
import datetime
import test_database_setup as tdb
from datetime import timedelta

class test_database_utils(unittest.TestCase):

	#The details of the database to be accessed
	HOST = "localhost"
	USER = "root"
	PASSWORD = "root"
	DATABASE = "People"

	#This sets up the test, namely by connecting to the database, clearing the table to be tested
	#And then populating the table
	#SetupClass is being used due to the need to connect to an external database
	def setUp(self):

		self.db = database.databaseUtils(test_database_utils.HOST, test_database_utils.USER, test_database_utils.PASSWORD, test_database_utils.DATABASE)
		self.conn = self.db.get_connection()

		tdb.clearDatabases(self.conn)
		tdb.createTables(self.conn)

	#This function removes is called at the end of the test and closes the connection 
	def tearDown(self):
		try:
			self.db.close_connection()
		except:
			pass
		finally:
			self.db = None

	#A helper method that provides the number of entries present
	def countPeople(self):
		with self.conn.cursor() as cursor:
			cursor.execute("select count(*) from user")
			count = cursor.fetchall()

			return count.pop()['count(*)']

	#Tests whether the insert function works, and that duplicate entries cannot be entered
	#Tests that the Primary Key of username works

	def test_insert_person(self):
		with self.db as db:

			count = self.countPeople()
			self.assertTrue(db.insert_user("Ralphie", "Ralpho", "Emmerson", "poetry", "ralph@deadpoet.com") == "success")
			self.assertTrue(count+1 == self.countPeople())
			self.assertTrue(db.insert_user("Ralphie", "Ralpho", "Emmerson", "poetry", "ralph@deadpoet.com") == "Email already used")
			self.assertTrue(count+1 == self.countPeople())
			self.assertTrue(db.insert_user("JoniBoi", "Pope", "John Paul II", "pope", "thepope@stpeters.vt") == "success")
			self.assertTrue(count+2 == self.countPeople())

	#Tests that the return user function works
	#This returns the username and the password
	def test_return_user(self):

		with self.db as db:

			self.assertTrue(len(db.return_user("john@password.com")) == 1)

	#Tests that the return user details works. This confirms that all of the details of the particular user
	#Is returned.
	def test_return_user_details(self):

		with self.db as db:

			user_details = db.return_user_details("john@password.com")
			user_details = user_details.pop()

			self.assertTrue(user_details['username'] == 'Johnno')
			self.assertTrue(user_details['firstname'] == 'John')
			self.assertTrue(user_details['lastname'] == 'Delaney')
			self.assertTrue(user_details['password'] == 'abc123')
			self.assertTrue(user_details['email'] == 'john@password.com')

	def test_singleton(self):

		singleton_database = singleton.Singleton(test_database_utils.HOST, test_database_utils.USER, test_database_utils.PASSWORD, test_database_utils.DATABASE)
		with self.assertRaises(Exception) as context:

			singleton_database2 = singleton.Singleton(test_database_utils.HOST, test_database_utils.USER, test_database_utils.PASSWORD, test_database_utils.DATABASE)
			self.assertTrue("You cannot create more than one connection!" in context.exception)

	def test_get_booking_history(self):

		with self.db as db:
			self.assertTrue(len(db.get_booking_history("john@password.com")) == 2)

	def test_get_available_local_cars(self):

		with self.db as db:

			self.assertTrue(len(db.get_available_cars(-37.800855,144.977234)) == 2)

	def test_get_all_available_case(self):
		with self.db as db:

			self.assertTrue(len(db.get_all_cars()) == 7)

	def test_get_vehicle_details(self):

		with self.db as db:

			vehicle_details = db.return_vehicle_details('XYZ987')

			vehicle_details = vehicle_details.pop()

			self.assertTrue(vehicle_details["rego"] == 'XYZ987')
			self.assertTrue(vehicle_details["make"] == 'Holden')
			self.assertTrue(vehicle_details["model"] == 'Commodore')
			self.assertEqual(float(vehicle_details['locationlong']), -37.799972)
			self.assertEqual(float(vehicle_details['locationlat']), 144.977393)
			self.assertTrue(vehicle_details['colour'] == 'green')
			self.assertTrue(vehicle_details['bodytype'] == 'Family')
			self.assertTrue(vehicle_details['seats'] == 5)
			self.assertTrue(float(vehicle_details['b.colour']) == 15.00)

	def test_book_vehicle(self):

		with self.db as db:

			pickup = datetime.datetime(2020,5,1,13)
			dropoff = pickup + timedelta(hours=4)

			test_result = "Vehicle Booked, your booking number is 4 and the price is $36.00"

			self.assertTrue(db.book_vehicle("john@password.com", "AH786B", pickup, dropoff) == test_result)
			self.assertTrue(len(db.get_booking_history("john@password.com")) == 3)

			pickup = datetime.datetime.now()
			pickup = pickup + timedelta(hours=1)
			dropoff = pickup + timedelta(hours = 3)
			self.assertTrue(db.book_vehicle("john@password.com", "U75PYV", pickup, dropoff) == "Vehicle already booked")

			pickup = datetime.datetime.now()
			pickup = pickup + timedelta(hours=-3)
			dropoff = pickup + timedelta(hours = 3)
			self.assertTrue(db.book_vehicle("john@password.com", "U75PYV", pickup, dropoff) == "Vehicle already booked")

	def test_cancel_booking(self):

		with self.db as db:

			pickup = datetime.datetime.now()
			pickup = pickup + timedelta(days= 2, hours=-2)
			dropoff = pickup + timedelta(days=2, hours=4)

			db.book_vehicle("fry@planetExpress.earth", "GHR445", pickup, dropoff)
			
			self.assertTrue(db.cancel_booking("fry@planetExpress.earth", 3) == "Can't cancel a booking in progress")
			self.assertTrue(db.cancel_booking("fry@planetExpress.earth", 4) == "Booking successfully cancelled")
			self.assertTrue(len(db.get_booking_history("fry@planetExpress.earth")) == 2)

			self.assertTrue(db.cancel_booking("john@password.com", 3) == "Can't cancel somebody else's booking")
			self.assertTrue(db.cancel_booking("john@password.com", 1) == "Can't cancel a previous booking")
			self.assertTrue(db.cancel_booking("john@password.com", 20) == "No booking exists")

			db.book_vehicle("john@password.com", "GHR445", pickup, dropoff)
			self.assertTrue(len(db.get_booking_history("john@password.com")) == 3)

	def test_search_vehicle(self):

		with self.db as db:

			self.assertTrue(len(db.return_vehicle_details('Holden')) == 2)
			self.assertTrue(db.return_vehicle_details('Holden').pop()['rego'] == 'XYZ987')
			self.assertTrue(len(db.return_vehicle_details('Commodore')) == 2)
			self.assertTrue(db.return_vehicle_details('Commodore').pop()['rego'] == 'XYZ987')
			self.assertTrue(len(db.return_vehicle_details('silver')) == 3)
			self.assertTrue(db.return_vehicle_details('silver').pop()['rego'] == 'GHR445')
			self.assertTrue(len(db.return_vehicle_details('Medium')) == 1)
			self.assertTrue(db.return_vehicle_details('Medium').pop()['rego'] == 'LMP675')
			self.assertTrue(len(db.return_vehicle_details('5')) == 5)
			self.assertTrue(db.return_vehicle_details('5').pop()['rego'] == 'YUPPIE')
			self.assertTrue(len(db.return_vehicle_details('Prestige Large')) == 1)
			self.assertTrue(db.return_vehicle_details('Prestige Large').pop()['rego'] == 'YUPPIE')

	def test_search_vehicle_location(self):

		with self.db as db:								
			self.assertTrue(len(db.return_vehicle_details_location(-37.800855,144.977234,'green')) == 1)
			self.assertTrue(db.return_vehicle_details_location(-37.800855,144.977234,'green').pop()['rego'] == 'XYZ987')
			self.assertTrue(len(db.return_vehicle_details_location(-37.800855,144.977234,'Toyota')) == 0)

if __name__ == "__main__":
    unittest.main()

