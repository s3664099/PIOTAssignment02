import sys
sys.path.insert(0,'..')

import unittest
import Database.database_utils as database
import Tests.test_database_setup as tdb
import pushbullet.pushbullet as pb
import pushbullet.create_qrcode as qr
import AgentPi.scan_barcode as bc

class test_database_utils(unittest.TestCase):

	#The details of the database to be accessed
	HOST = "localhost"
	USER = "root"
	PASSWORD = "root"
	DATABASE = "People"
	PB_KEY = ''
	file = "key.txt"

	#This sets up the test, namely by connecting to the database, clearing the table to be tested
	#And then populating the table
	#SetupClass is being used due to the need to connect to an external database
	def setUp(self):

		key = open(self.file,'r')
		self.PB_KEY = key.readline()
		key.close()

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

	def test_pushbullet(self):

		self.assertTrue(pb.send_notification("Hello There","How's it going dude?",self.PB_KEY) == "Notification sent")


	def test_pushbullet_message(self):
		with self.db as db:

			db.add_engineer('S.I@carshare.com','EE:6E:FF:22:2b:36',self.PB_KEY)

			key = db.get_token('S.I@carshare.com').pop()

			car = db.return_vehicle_details('XYZ987').pop()

			title = "Service Required"
			message = "Vehicle Rego: {}, {}, {}, {}".format(car['rego'],car['colour'], car['make'], car['model'])

			self.assertTrue(pb.send_notification(title,message,key['pb_token']) == "Notification sent")

	def test_qr_code_creator(self):

		with self.db as db:

			db.create_employee('SJanitor','Janitor','Scruffy','mybucket','J.S@carshare.com','Engineer')
			db.add_engineer('S.J@carshare.com','EE:6E:FF:22:2b:36',self.PB_KEY)

			engineer = db.get_engineer_details('S.J@carshare.com').pop()

			self.assertTrue(qr.create_qr_code(engineer['firstname'], engineer['lastname'], engineer['email']) == "QR code created")	

	def test_scan_barcode(self):

		details = bc.read_qr_no_webcam()
		details = details.split(' ')

		self.assertTrue(bc.read_qr_no_webcam() == "First Name: Janitor, Surname: Scruffy, email J.S@carshare.com")

	#def test_scan_barcode_webcam(self):

		#self.assertTrue(bc.read_qr_webcam('Janitor','Scruffy') == "First Name: Janitor, Surname: Scruffy, email J.S@carshare.com")

if __name__ == "__main__":
    unittest.main()