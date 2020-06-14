import sys
sys.path.insert(0,'..')

import unittest
import AgentPi.unlock_car as uc

class test_database_utils(unittest.TestCase):

	def test_bluetooth(self):

		address = [{"mac_address": "60:14:B3:C1:5B:22",
			"name": "Professor Farnsworth"}]

		self.assertTrue(uc.scan_devices(address) == "Greetings Professor Farnsworth. The car is unlocked")

	def test_db(self):
		con = uc.create_db()

		self.assertTrue(uc.insert_engineer(con, "Professor Farnsworth","60:14:B3:C1:5B:22") == "Engineer details inserted")

		engineers = uc.get_engineer(con)
		engineer = engineers.pop()

		self.assertTrue(engineer['name'] == "Professor Farnsworth")
		self.assertTrue(engineer['mac_address'] == "60:14:B3:C1:5B:22")

	def test_db_bluetooth(self):

		con = uc.create_db()
		uc.insert_engineer(con, "Professor Farnsworth","60:14:B3:C1:5B:22")
		self.assertTrue(uc.scan_devices(uc.get_engineer(con)) == "Greetings Professor Farnsworth. The car is unlocked")

		uc.close_db(con)


if __name__ == "__main__":
    unittest.main()