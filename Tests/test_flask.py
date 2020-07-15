import sys
sys.path.insert(0,'..')

import unittest
import Database.database_utils as database
import Tests.test_database_setup as tdb
import requests

class test_database_utils(unittest.TestCase):

	#The details of the database to be accessed
	HOST = "localhost"
	USER = "root"
	PASSWORD = "root"
	DATABASE = "People"
	PB_KEY = ''
	file = "key.txt"

	def test_getusername(self):

		self.assertTrue(requests.get("http://192.168.3.3:5000/username/email@email.com").json() == "DaveSarkies")

	def test_getorderhistory(self):

		email = "s3664099@student.rmit.edu.au"

		self.assertTrue(len(requests.get("http://192.168.3.3:5000/orderhistory/"+email).json()) == 5)

	def test_confirmedbookings(self):

		email = "s3664099@student.rmit.edu.au"

		self.assertTrue(len(requests.get("http://192.168.3.3:5000/confirmedbookings/"+email).json()) == 3)

	def test_availablecars(self):

		self.assertTrue(len(requests.get("http://192.168.3.3:5000/availablecars").json())==1)

	def test_searchcars(self):

		search = "red"
		self.assertTrue(len(requests.get("http://192.168.3.3:5000/searchcar/"+search).json()) == 1)

		search = "family"
		self.assertTrue(len(requests.get("http://192.168.3.3:5000/searchcar/"+search).json()) == 1)

	def test_get_user_details(self):

		email = "s3664099@student.rmit.edu.au"

		self.assertTrue(requests.get("http://192.168.3.3:5000/finduserdetails/"+email).json().pop()['is_active'] == 1)
		self.assertTrue(requests.get("http://192.168.3.3:5000/finduserdetails/"+email).json().pop()['username'] == "DavidS")
		self.assertTrue(requests.get("http://192.168.3.3:5000/finduserdetails/"+email).json().pop()['role'] == "Customer")

		email = "bender@bending.net"
		self.assertTrue(requests.get("http://192.168.3.3:5000/finduserdetails/"+email).json().pop()['is_active'] == 1)
		self.assertTrue(requests.get("http://192.168.3.3:5000/finduserdetails/"+email).json().pop()['username'] == "BenderRodregez")
		self.assertTrue(requests.get("http://192.168.3.3:5000/finduserdetails/"+email).json().pop()['role'] == "Engineer")

	def test_get_user_role(self):

		email = "bender@bending.net"
		role = "Engineer"

		self.assertTrue(requests.get("http://192.168.3.3:5000/role/"+role+"/"+email).json() == "Success")

		email = "s3664099@student.rmit.edu.au"
		role = "Noob"
		self.assertTrue(requests.get("http://192.168.3.3:5000/role/"+role+"/"+email).json() == "Error")

if __name__ == "__main__":
    unittest.main()