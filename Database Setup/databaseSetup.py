#Python DataBase Setup
#=====================
#
#This script is designed to take the contents of a specific txt
#file, created from a spreadsheet, and create a database around it.
#The initial database is cleared, and the contents of the file are then
#placed into the database.
#
#Try/Except statements are used for error handling, and are essential
#when working with databases (as is the case with files)

#This is required for python3 to create and manipulate mySql databases
import pymysql

hostname = '35.197.174.1'
username = 'root'
password = 'password'
database = 'People'

#This function clears the database
def clearDatabases(conn):
	cur = conn.cursor()

	#Foreign Key checks are turned off to allow the tables
	#to be cleared, and dropped.
	cur.execute("SET FOREIGN_KEY_CHECKS = 0")
	
	try:
		cur.execute("DROP TABLE car")
	except:
		print("No such table as car")

	try:
		cur.execute("DROP TABLE user")
	except:
		print("No such table as user")
	try:
		cur.execute("DROP TABLE makemodel")
	except:
		print("No such table as makemodel")
	try:
		cur.execute("DROP TABLE bodytype")
	except:
		print("No such table as bodytype")	
	try:
		cur.execute("DROP TABLE booking")
	except:
		print("No such table as booking")

#This function creates the tables associated with the database
def createTables(conn):
	cur = conn.cursor()

	try:
		cur.execute("CREATE TABLE bodytype (bodytype VARCHAR(20), seats INTEGER(2), hourlyPrice DECIMAL(4,2), icon VARCHAR(20), PRIMARY KEY (bodytype))")
	except pymysql.Error as e:
		print("Error 01: {}", e)

	try:
		cur.execute("CREATE TABLE makemodel (make VARCHAR(20), model VARCHAR(20), bodytype VARCHAR(20), PRIMARY KEY (make,model), FOREIGN KEY (bodytype) REFERENCES bodytype(bodytype))")
	except pymysql.Error as e:
		print("Error 02: {}", e)

	try:
		cur.execute("CREATE TABLE car (rego VARCHAR(10), make VARCHAR(20), model VARCHAR(20), locationLong DECIMAL(9,6), locationLat DECIMAL(9,6), colour VARCHAR(10), PRIMARY KEY (rego), FOREIGN KEY (make, model) REFERENCES makemodel(make, model))")
	except pymysql.Error as e:
		print("Error 03: {}", e)

	try:
		cur.execute("CREATE TABLE user (username VARCHAR(20), firstname VARCHAR(20), lastname VARCHAR(20), password VARCHAR(20), email VARCHAR(28), PRIMARY KEY (username))")
	except pymysql.Error as e:
		print("Error 04: {}", e)
	try:
		cur.execute("CREATE TABLE booking(bookingnumber INT NOT NULL AUTO_INCREMENT, rego VARCHAR(10), username VARCHAR(20), pickuptime DATETIME, dropofftime DATETIME, totalcost DECIMAL (4,2), PRIMARY KEY (bookingnumber), FOREIGN KEY (rego) REFERENCES car(rego), FOREIGN KEY (username) REFERENCES user(username))")
	except pymysql.Error as e:
		print("Error 05: {}", e)

	#The database is populated
	try:
		cur.execute("INSERT INTO bodytype VALUES ('Compact', '2', '5.00','compact.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Hatchback', '4', '7.00','hatchback.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Small', '4', '9.00','small.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Medium', '5', '13.00','medium.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Family', '5', '15.00','family.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Station Wagon', '5', '20.00','stationwagon.png')")
		cur.execute("INSERT INTO bodytype VALUES ('SUV Small', '4', '15.00','suv.png')")
		cur.execute("INSERT INTO bodytype VALUES ('SUV Large', '5', '25.00','suv.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Van', '2', '15.00','van.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Family Van', '8', '25.00','van.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Mini-Van', '15', '35.00','minivan.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Presige Small', '4', '35.00','prestige.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Prestige Large', '5', '55.00','prestige.png')")
		cur.execute("INSERT INTO bodytype VALUES ('Sports', '2', '55.00','sportscar.png')")

		cur.execute("INSERT INTO makemodel VALUES ('Holden', 'Commodore', 'Family')")
		cur.execute("INSERT INTO makemodel VALUES ('Ford', 'Falcon', 'Family')")
		cur.execute("INSERT INTO makemodel VALUES ('Toyota', 'Yaris', 'Small')")
		cur.execute("INSERT INTO makemodel VALUES ('Ford', 'Festiva', 'Hatchback')")
		cur.execute("INSERT INTO makemodel VALUES ('Toyota', 'Camry', 'Medium')")
		cur.execute("INSERT INTO makemodel VALUES ('Toyota', 'Rav 4', 'SUV Small')")
		cur.execute("INSERT INTO makemodel VALUES ('BMW', 'X22', 'Prestige Small')")
		cur.execute("INSERT INTO makemodel VALUES ('BMW', 'F32', 'Prestige Large')")
		cur.execute("INSERT INTO makemodel VALUES ('Ferrari', 'Testorosa', 'Sports')")
		cur.execute("INSERT INTO makemodel VALUES ('Holden', 'Spark', 'Compact')")
		cur.execute("INSERT INTO makemodel VALUES ('Holden', 'Astra', 'Hatchback')")
		cur.execute("INSERT INTO makemodel VALUES ('Holden', 'Barina', 'Small')")
	except pymysql.Error as e:
		print("Error 06: {}", e)

	conn.commit()	

		
#This function exists to test that the contents of the database were updated sufficiently
#Also for error handling
def testQuery(conn):
	cur = conn.cursor()

	try:
		cur.execute("SHOW TABLES")

		for table in cur.fetchall():
			print(table)
	except:
		print("Error")

	try:
		cur.execute("SELECT bodytype, seats, hourlyPrice FROM bodytype")

		for bodytype, seats, hourlyPrice in cur.fetchall():
			print(bodytype+" "+str(seats)+" "+" "+str(hourlyPrice))
	except:
		print("Error")

	try:
		cur.execute("SELECT make, model, bodytype FROM makemodel")

		for make, model, bodytype in cur.fetchall():
			print(make+" "+model+" "+" "+bodytype)
	except:
		print("Error")


print("Connecting")
#The main function. The database is opened, and the functions are executed
myConnection = pymysql.connect(host=hostname, user = username, passwd = password, db = database, charset='utf8')
cur = myConnection.cursor()
print("Connected")

cur.execute('SET NAMES utf8')
cur.execute('SET CHARACTER SET utf8')
cur.execute('SET character_set_connection=utf8')

clearDatabases(myConnection)
createTables(myConnection)
#loadDataFile(myConnection)
testQuery(myConnection)
myConnection.close()


