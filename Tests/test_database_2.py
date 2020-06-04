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

			self.assertTrue(employee['role'] == 'MANAGER')
			self.assertTrue(employee['email'] == 'H.F@carshare.com')

	def test_get_employee_type(self):

		print("Test get employee type")

		with self.db as db:

			db.create_employee('Hubert','Farnsworth','password','0444000111','MANAGER')
			db.create_employee('Hermes','Conrad','password','0444000111','ADMIN')
			db.create_employee('Scruffy','Janitor','password','0444000111','ENGINEER')
			db.create_employee('Taronga','Leelha','password','0444000111','ENGINEER')
			db.create_employee('Zap','Brannigan','password','0444000111','ADMIN')
			db.create_employee('Richard','Nixon','password','0444000111','MANAGER')
			db.create_employee('Spiro','Agnew','password','0444000111','MANAGER')

			self.assertTrue(len(db.return_employee_type('MANAGER'))==3)
			self.assertTrue(len(db.return_employee_type('ADMIN'))==2)
			self.assertTrue(len(db.return_employee_type('ENGINEER'))==2)
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

			db.add_engineer('S.J@carshare.com','EE:6E:FE:22:2b:36')

			self.assertTrue(db.get_mac_address('S.J@carshare.com').pop()['mac_address'] == 'EE:6E:FE:22:2b:36')
			self.assertTrue(db.get_engineer('C.B@carshare.com') == "No engineer found with that email")
			self.assertTrue(db.get_mac_address('C.B@carshare.com') == "No engineer found with that email")

	def test_get_all_mac_addresses(self):

		with self.db as db:

			db.add_engineer('S.I@carshare.com','EE:6E:FF:22:2b:36')
			db.add_engineer('S.J@carshare.com','EE:6E:FE:22:2b:36')
			db.add_engineer('T.J@carshare.com','EF:6E:FE:22:2b:36')
			db.add_engineer('Q.J@carshare.com','EE:6E:FE:23:2b:36')

			self.assertTrue(len(db.get_all_mac_addresses()) == 4)
			self.assertTrue(db.get_all_mac_addresses().pop()['mac_address']== 'EF:6E:FE:22:2b:36')

	def test_service_request(self):

		with self.db as db:

			self.add_engineer(db)

			self.assertTrue(db.create_service_request('U75PYV', 3000, 'H.C@carshare.com') == 'car booked for service. The service number is 1')
			self.assertTrue(db.create_service_request('PPPQQQ', 3000, 'H.C@carshare.com') == 'Unable to book vehicle for service, no such vehicle exists')
			self.assertTrue(db.create_service_request('U75PYV', 3000, 'P.Q@email.com') == 'Invalid email. Unable to book vehicle for service')
			self.assertTrue(db.create_service_request('U75PYV', 3000, 'H.C@carshare.com') == 'A service request has already been booked for vehicle U75PYV')

	def test_get_service_request(self):

		with self.db as db:

			self.add_engineer(db)

			db.create_service_request('U75PYV', 3000, 'H.C@carshare.com')
			db.create_service_request('AH786B', 3000, 'H.C@carshare.com')
			db.create_service_request('LMP675', 3000, 'H.C@carshare.com')

			self.assertTrue(db.get_service_request(1).pop()['rego'] == 'U75PYV')
			self.assertTrue(db.get_service_request(4) == 'No service request found with id 4')
			self.assertTrue(len(db.get_all_service_requests()) == 3)
			self.assertTrue(len(db.get_all_unassigned_service_requests()) == 3)
			self.assertTrue(len(db.get_all_active_service_requests()) == 3)

	def test_assign_engineer(self):

		with self.db as db:

			self.add_engineer(db)
			
			db.create_service_request('U75PYV', 3000, 'H.C@carshare.com')
			db.create_service_request('AH786B', 3000, 'H.C@carshare.com')
			db.create_service_request('LMP675', 3000, 'H.C@carshare.com')

			self.assertTrue(len(db.get_all_unassigned_service_requests()) == 3)
			self.assertTrue(db.assign_engineer('S.J@carshare.com',1) == "Engineer successfully assigned")
			self.assertTrue(db.assign_engineer('S.J@carshare.com',1) == "engineer already assigned to this service request")
			self.assertTrue(db.assign_engineer('S.J@carshare.com',5) == "No service request found with id 5")
			self.assertTrue(db.assign_engineer('P.P@carshare.com',2) == "No engineer found with email P.P@carshare.com") 
			self.assertTrue(len(db.get_all_unassigned_service_requests()) == 2)

	def add_engineer(self, db):

		db.create_employee('Hermes','Conrad','password','0444000111','ADMIN')
		db.add_engineer('S.J@carshare.com','EE:6E:FE:22:2b:36')	

	def assign_engineer(self, db):

		db.create_service_request('U75PYV', 3000, 'H.C@carshare.com')
		db.create_service_request('AH786B', 3000, 'H.C@carshare.com')
		db.create_service_request('LMP675', 3000, 'H.C@carshare.com')
		db.assign_engineer('S.J@carshare.com',1)

	def test_service_complete(self):

		with self.db as db:

			self.add_engineer(db)
			self.assign_engineer(db)
		
			db.create_service_request('U75PYV', 3000, 'H.C@carshare.com')
			db.create_service_request('AH786B', 3000, 'H.C@carshare.com')
			db.create_service_request('LMP675', 3000, 'H.C@carshare.com')
			db.assign_engineer('S.J@carshare.com',1)

			self.assertTrue(len(db.get_all_active_service_requests()) == 3)
			self.assertTrue(db.service_complete(1) == "Service completed")						
			self.assertTrue(len(db.get_all_active_service_requests()) == 2)
			self.assertTrue(db.service_complete(4) == "No service request found with id 4")
			self.assertTrue(db.service_complete(2) == "No engineer assigned to this service request")
			self.assertTrue(db.service_complete(1) == "Service request not active")

		
if __name__ == "__main__":
    unittest.main()

