import unittest
import db_singleton as singleton
import database_utils as database

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

		#The SQL and the table population is performed here
		with self.conn.cursor() as cur:
			cur.execute("DROP TABLE if exists user")
			cur.execute("CREATE TABLE if not exists user (username VARCHAR(20), firstname VARCHAR(20), lastname VARCHAR(20), password VARCHAR(20), email VARCHAR(28), PRIMARY KEY (username))")
			cur.execute("INSERT INTO user VALUES ('Johnno', 'John','Delaney','abc123','john@password.com') ")
			cur.execute("INSERT INTO user VALUES ('Fry', 'Philip','Fry','Leelha','fry@planetExpress.earth') ")
		self.conn.commit()

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


if __name__ == "__main__":
    unittest.main()

