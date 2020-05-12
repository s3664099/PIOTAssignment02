import sys
sys.path.append('../')
sys.path.append('../AgentPi')

import unittest
import sqlite_utils as sqlite
import test_sqlite_setup as setup

host = "test.db"

class test_sqlite_utils(unittest.TestCase):

	def setUp(self):
		setup.setup()
		self.db = sqlite.sqlite_utils(host)

	def test_setup(self):
		self.assertTrue(len(self.db.get_all_users())==2)

	def test_get_user_name(self):
		user = self.db.get_user('Geralt')
		user = user.pop()

		self.assertTrue(user[0]=='Geralt')
		self.assertTrue(user[1]=='Witcher')
		self.assertTrue(user[2]=='Geralt')
		self.assertTrue(user[3]=='of Rivia')
		self.assertTrue(user[4]=='geralt@rivia.net')

	def test_get_user_password(self):
		user = self.db.get_user('geralt@rivia.net')
		user = user.pop()

		self.assertTrue(user[0]=='Geralt')
		self.assertTrue(user[1]=='Witcher')
		self.assertTrue(user[2]=='Geralt')
		self.assertTrue(user[3]=='of Rivia')
		self.assertTrue(user[4]=='geralt@rivia.net')

	def test_insert_user(self):

		self.assertTrue(len(self.db.get_all_users())==2)
		self.db.insert_user("Pinky","hamstring32","Pinky","Pig Bottom","pinky@harvard.edu")

		self.assertTrue(len(self.db.get_user('Pinky'))==1)
		self.assertTrue(len(self.db.get_all_users())==3)



if __name__ == "__main__":
    unittest.main()