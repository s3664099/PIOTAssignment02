import pymysql

#A class for creating a connection to the database to enable manipulation
#and retrieval.
class databaseUtils:
	HOST = ""
	USER = ""
	PASSWORD = ""
	DATABASE = ""
	connection = None

	#Establishes the connection by passing through the required variables
	#The variables aren't hardcoded to enable testing on a test database
	def __init__ (self, host, user, password, database):
		databaseUtils.HOST = host
		databaseUtils.USER = user
		databaseUtils.PASSWORD = password
		databaseUtils.DATABASE = database

		#This is where the connection is made, and saved as a variable in the class
		if databaseUtils.connection == None:
			myConnection = pymysql.connect(host=databaseUtils.HOST, user = databaseUtils.USER, passwd = databaseUtils.PASSWORD, 
    			db = databaseUtils.DATABASE, charset='utf8')
		self.connection = myConnection

	#The following methods are for closing the database
	def close_connection(self):

		self.connection.close()

	def __enter__ (self):
		return self

	def __exit__(self, type, value, traceback):
		self.close_connection()

	#This returns the connection to the database to enable a connection elsewhere
	def get_connection(self):
		return self.connection

	#This method is designed to insert a new user into the database
	def insert_user(self, user_name, first_name, last_name, password, email):
		with self.connection.cursor() as cur:
			response = "success"
			try:
				cur.execute("INSERT INTO user VALUES ('"+user_name+"','"+first_name+"','"+last_name+"','"+password+"','"+email+"')")
			except:
				response = "User name already used"
			self.connection.commit()
			return response

	#This method returns the password and the user name of the user
	def return_user(self, user_name):
		with self.connection.cursor() as cur:
			cur.execute("SELECT username, password FROM user WHERE username='"+user_name+"'")
			return cur.fetchall()

	#Return user details
	def return_user_details(self, user_name):
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM user WHERE username='"+user_name+"'")

			return cur.fetchall()		









