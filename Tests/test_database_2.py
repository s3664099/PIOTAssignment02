import sys
sys.path.insert(0,'..')

import unittest
import db_singleton as singleton
import Database.database_utils as database
import datetime
import Tests.test_database_setup as tdb
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
			print("Test Insert")
			count = self.countPeople()
			self.assertTrue(db.insert_user("Ralphie", "Ralpho", "Emmerson", "poetry", "ralph@deadpoet.com") == "success")
			self.assertTrue(count+1 == self.countPeople())
			self.assertTrue(db.insert_user("Ralphie", "Ralpho", "Emmerson", "poetry", "ralph@deadpoet.com") == "Email already used")
			self.assertTrue(count+1 == self.countPeople())
			self.assertTrue(db.insert_user("JoniBoi", "Pope", "John Paul II", "pope", "thepope@stpeters.vt") == "success")
			self.assertTrue(count+2 == self.countPeople())

	def test_insert_employee(self):

		with self.db as db:

			print("Test insert employee")

			self.assertTrue(db.create_employee('Hubert','Farnsworth','password','0444000111','MANAGER') == 'success')
			self.assertTrue(db.create_employee('Hubert','Farnsworth','password','0444000111','MANAGER') == 'Email already used')
			self.assertTrue(db.create_employee('Taronga','Leehla','password','0444000111','STARSHIP CAPTAIN') == 'invalid role')

	def test_get_employee(self):

		with self.db as db:

			db.create_employee('Hubert','Farnsworth','password','0444000111','MANAGER')

			employee = db.return_employee('H.F@carshare.com')
			employee = employee.pop()

			self.assertTrue(employee['username'] == 'HubertFarnsworth')
			self.assertTrue(employee['role'] == 'MANAGER')
			self.assertTrue(employee['email'] == 'H.F@carshare.com')

	def test_get_employee_type(self):

		print("Test get employee type")

		with self.db as db:

			db.create_employee('Hubert','Farnsworth','password','0444000111','MANAGER')
			db.create_employee('Hermes','Conrad','password','0444000111','ADMIN')
			db.create_employee('Scruffy','Janitor','password','0444000111','MECHANIC')
			db.create_employee('Taronga','Leelha','password','0444000111','MECHANIC')
			db.create_employee('Zap','Brannigan','password','0444000111','ADMIN')
			db.create_employee('Richard','Nixon','password','0444000111','MANAGER')
			db.create_employee('Spiro','Agnew','password','0444000111','MANAGER')

			self.assertTrue(len(db.return_employee_type('MANAGER'))==3)
			self.assertTrue(len(db.return_employee_type('ADMIN'))==2)
			self.assertTrue(len(db.return_employee_type('MECHANIC'))==2)
			self.assertTrue(len(db.return_all_employees())==7)

	def test_activate_employee(self):

		print("Test activate employee")

		with self.db as db:

			db.create_employee('Hubert','Farnsworth','password','0444000111','MANAGER')

			self.assertTrue(db.activate_employee("H.F@carshare.com") == "success")

			self.assertTrue(db.activate_employee("P.Q@carshare.com") == "user not found")

	def test_add_engineer(self):

		print("Test Engineer")

		with self.db as db:

			db.add_engineer('S.J@carshare.com','ScruffyJanitor','EE:6E:FE:22:2b:36')

			self.assertTrue(db.get_engineer('S.J@carshare.com').pop()['username'] == 'ScruffyJanitor')
			self.assertTrue(db.get_mac_address('S.J@carshare.com').pop()['mac_address'] == 'EE:6E:FE:22:2b:36')
			self.assertTrue(db.get_engineer('C.B@carshare.com') == "No engineer found with that email")
			self.assertTrue(db.get_mac_address('C.B@carshare.com') == "No engineer found with that email")

	def test_get_all_mac_addresses(self):

		with self.db as db:

			db.add_engineer('S.I@carshare.com','ScruffyJanitor','EE:6E:FF:22:2b:36')
			db.add_engineer('S.J@carshare.com','ScruffyJanitor','EE:6E:FE:22:2b:36')
			db.add_engineer('T.J@carshare.com','ScruffyJanitor','EF:6E:FE:22:2b:36')
			db.add_engineer('Q.J@carshare.com','ScruffyJanitor','EE:6E:FE:23:2b:36')

			self.assertTrue(len(db.get_all_mac_addresses()) == 4)
			self.assertTrue(db.get_all_mac_addresses().pop()['mac_address']== 'EF:6E:FE:22:2b:36')


		
if __name__ == "__main__":
    unittest.main()

