import unittest
#import pymysql
import db_singleton as singleton
import database_utils as database
import datetime
import test_database_setup as tdb
from datetime import timedelta

class test_database_utils(unittest.TestCase):

	#The details of the database to be accessed
	HOST = "35.197.174.1"
	USER = "root"
	PASSWORD = "password"
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
			return cursor.fetchone()[0]

	#Tests whether the insert function works, and that duplicate entries cannot be entered
	#Tests that the Primary Key of username works
	def test_insert_person(self):
		with self.db as db:

			count = self.countPeople()
			self.assertTrue(db.insert_user("Ralphie", "Ralpho", "Emmerson", "poetry", "ralph@deadpoet.com") == "success")
			self.assertTrue(count+1 == self.countPeople())
			self.assertTrue(db.insert_user("Ralphie", "Ralpho", "Emmerson", "poetry", "ralph@deadpoet.com") == "User name already used")
			self.assertTrue(count+1 == self.countPeople())
			self.assertTrue(db.insert_user("JoniBoi", "Pope", "John Paul II", "pope", "thepope@stpeters.vt") == "success")
			self.assertTrue(count+2 == self.countPeople())

	#Tests that the return user function works
	#This returns the username and the password
	def test_return_user(self):

		with self.db as db:
			self.assertTrue(len(db.return_user("Johnno")) == 1)

	#Tests that the return user details works. This confirms that all of the details of the particular user
	#Is returned.
	def test_return_user_details(self):

		with self.db as db:

			user_details = db.return_user_details("Johnno")

			self.assertTrue(user_details[0][0] == 'Johnno')
			self.assertTrue(user_details[0][1] == 'John')
			self.assertTrue(user_details[0][2] == 'Delaney')
			self.assertTrue(user_details[0][3] == 'abc123')
			self.assertTrue(user_details[0][4] == 'john@password.com')

	def test_singleton(self):

		singleton_database = singleton.Singleton(test_database_utils.HOST, test_database_utils.USER, test_database_utils.PASSWORD, test_database_utils.DATABASE)
		with self.assertRaises(Exception) as context:
			singleton_database2 = singleton.Singleton(test_database_utils.HOST, test_database_utils.USER, test_database_utils.PASSWORD, test_database_utils.DATABASE)
			self.assertTrue("You cannot create more than one connection!" in context.exception)

	def test_get_booking_history(self):

		with self.db as db:
			self.assertTrue(len(db.get_booking_history("Johnno")) == 2)

	def test_get_available_cars(self):

		with self.db as db:
			self.assertTrue(len(db.get_available_cars(-37.800855,144.979234)) == 2)

	def test_get_vehicle_details(self):

		with self.db as db:
			vehicle_details = db.return_vehicle_details('XYZ987')

			self.assertTrue(vehicle_details[0][0] == 'XYZ987')
			self.assertTrue(vehicle_details[0][1] == 'Holden')
			self.assertTrue(vehicle_details[0][2] == 'Commodore')
			self.assertTrue(vehicle_details[0][3] == -37.799972)
			self.assertTrue(vehicle_details[0][4] == 144.977393)
			self.assertTrue(vehicle_details[0][5] == 'green')

	def test_book_vehicle(self):

		with self.db as db:

			pickup = datetime.datetime(2020,5,1,13)
			dropoff = pickup + timedelta(hours=4)

			self.assertTrue(db.book_vehicle("Johnno", "AH786B", pickup, dropoff) == "Vehicle Booked, your booking number is 4")
			self.assertTrue(len(db.get_booking_history("Johnno")) == 3)

			pickup = datetime.now()
			pickup = pickup + timedelta(hours=1)
			dropoff = pickup + timedelta(hours = 3)
			self.assertTrue(db.book_vehicle("Johnno", "AH786B", pickup, dropoff) == "Vehicle alredy booked")

	def test_cancel_booking(self):

		with self.db as db:
			self.assertTrue(db.cancel_booking("Fry", 2) == "Booking successfully cancelled")
			self.assertTrue(len(db.get_booking_history("Fry")) == 1)

			with self.assertRaises(Exception) as context:
				db.cancel_booking("Johnno", 2)
				self.assertTrue("Not your booking" in context.exception)
				db.cancel_booking("Johnno", 0)
				self.assertTrue("Can't cancel a Previous booking" in context.exception)




if __name__ == "__main__":
    unittest.main()

