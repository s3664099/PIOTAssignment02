import sys
sys.path.append('../')
sys.path.append('../Database')

import unittest
import pymysql
import login as login



class test_utils(unittest.TestCase):

	db = None

	def setUp(self):

		# Declaring the model
		# This should be in a config.json file, and the 
		db_hostname = 'localhost'
		db_username = 'root'
		db_password = 'root'
		database = 'People'

		# The main function. The database is opened, and the functions are executed
		self.db = pymysql.connect(host=db_hostname, user=db_username, passwd=db_password, db=database, charset='utf8mb4')

		cur = self.db.cursor()
		cur.execute('SET NAMES utf8mb4')
		cur.execute('SET CHARACTER SET utf8mb4')
		cur.execute('SET character_set_connection=utf8mb4')
		cur.close()

	def test_hash_password(self):

		password = "password"
		hashed_password = login.hash_password(password)

		self.assertTrue(login.verify_password(hashed_password,password) == True)

	#This tests that one of the password verification systems works
	def test_verify_password(self):

		password = "password"
		hashed_password = login.hash_password(password)

		self.assertTrue(login.verify_password(hashed_password,hashed_password) == False)
		self.assertTrue(login.verify_password(hashed_password,password) == True)

	#This tests that the function to retrieve an entry works
	def test_verify_user(self):

		#login.new_user("dave", "David", "Sarkies", "dasarkies@email.net","password",self.db)

		self.assertTrue(login.verify_register("dasarkies@email.net","password", self.db) == 1)

	#The test confirms that the password that is retrieved is correct
	def test_hashing_password(self):

		self.assertTrue(login.hashing_password("dasarkies@email.net","password", self.db) == "3f2da0032d8b0461661c0ee2ee240a88087c6a85e860b220a5ad29c6ea9ddb167bd5f4cf4e50fd56c8078a6c48e67c4397556df95af14d304f5adb491f6592e7")		

	def test_verify_password_new(self):

		stored_password = "3f2da0032d8b0461661c0ee2ee240a88087c6a85e860b220a5ad29c6ea9ddb167bd5f4cf4e50fd56c8078a6c48e67c4397556df95af14d304f5adb491f6592e7"
		provided_password = stored_password[64:]

		self.assertTrue(login.verify_password_new(stored_password, provided_password) == True)
		self.assertTrue(login.verify_password_new(stored_password, stored_password) == False)

	def test_login(self):

		password = "3f2da0032d8b0461661c0ee2ee240a88087c6a85e860b220a5ad29c6ea9ddb167bd5f4cf4e50fd56c8078a6c48e67c4397556df95af14d304f5adb491f6592e7"

		self.assertTrue(login.login("dasarkies@email.net",password, self.db) == 2)
		self.assertTrue(login.login("dasarkies@email.net","twinkle", self.db) == 3)

if __name__ == "__main__":
    unittest.main()

