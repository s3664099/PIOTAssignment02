import sqlite3

#Source: https://docs.python.org/3/library/sqlite3.html
class sqlite_utils:
	DB_NAME = None
	connection = None

	#Creates a connection to the database
	def __init__ (self, host):
		self.DB_NAME = host
		self.connection = sqlite3.connect(self.DB_NAME)

	def close_connection(self):
		self.connection.close()


	#Function to insert a user into the database.
	#This function is called if the user is not stored locally
	def insert_user(self, user_name, password, first_name, last_name, email):

		with self.connection as conn:
			cur = conn.cursor()

			cur.execute("INSERT into User Values ('"+user_name+"','"+password+"','\
    					"+first_name+"','"+last_name+"','"+email+"')")
			conn.commit()

	#Returns details of all users from the database
	#Primarily used for testing purposes only
	def get_all_users(self):

		with self.connection as conn:
			cur = conn.cursor()
			cur.execute("select * from User")

			return cur.fetchall()

	#Returns the details of the user from the database
	#The user can be search for by using either email or username
	def get_user(self, user_name):

		with self.connection as conn:
			query = "select password from User"
			cur = conn.cursor()

			cur.execute(query+" where username = ?", (user_name,))
			rows = cur.fetchall()

			#If the email was entered then the above query will
			#Return empty, so another search is performed by email
			if len(rows) == 0:
				cur.execute(query+" where email = ?", (user_name,))
				rows = cur.fetchall()

			return rows