import unittest
import login

class test_utils(unittest.TestCase):

	def test_hash_password(self):

		password = "password"
		hashed_password = login.hash_password(password)

		print(hashed_password)
		print(login.retrieve_password(hashed_password,password))

		self.assertTrue(login.retrieve_password(hashed_password,password) == hashed_password)

	def test_verify_password(self):

		password = "password"
		hashed_password = login.hash_password(password)

		self.assertTrue(login.verify_password(hashed_password,hashed_password) == True)
		self.assertTrue(login.verify_password(hashed_password,password) == False)



if __name__ == "__main__":
    unittest.main()

