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
database_used = 'car_app_db'
import datetime
from datetime import timedelta
import database_utils as database

db = database.databaseUtils(hostname, username, password, database_used)

##This function clears the database
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
	except pymysql.Error as e:
		print("Error 01: {}", e)		

#This function creates the tables associated with the database
def createTables(conn):
	cur = conn.cursor()

	try:
		cur.execute("CREATE TABLE bodytype (bodytype VARCHAR(20), seats INTEGER(2), hourlyPrice DECIMAL(4,2),\
					icon VARCHAR(20), PRIMARY KEY (bodytype))")
	except pymysql.Error as e:
		print("Error 01: {}", e)

	try:
		cur.execute("CREATE TABLE makemodel (make VARCHAR(20), model VARCHAR(20), bodytype VARCHAR(20),\
					PRIMARY KEY (make,model), FOREIGN KEY (bodytype) REFERENCES bodytype(bodytype))")
	except pymysql.Error as e:
		print("Error 02: {}", e)

	try:
		cur.execute("CREATE TABLE car (rego VARCHAR(10), make VARCHAR(20), model VARCHAR(20), locationLong DECIMAL(9,6),\
					locationLat DECIMAL(9,6), colour VARCHAR(10), PRIMARY KEY (rego), FOREIGN KEY (make, model)\
					REFERENCES makemodel(make, model))")
	except pymysql.Error as e:
		print("Error 03: {}", e)

	try:
		cur.execute("CREATE TABLE user (username VARCHAR(20), firstname VARCHAR(20), lastname VARCHAR(20),\
					password VARCHAR(192), email VARCHAR(28), PRIMARY KEY (email))")
	except pymysql.Error as e:
		print("Error 04: {}", e)
	try:
		cur.execute("CREATE TABLE booking(bookingnumber INT NOT NULL AUTO_INCREMENT, rego VARCHAR(10),\
					email VARCHAR(28), pickuptime DATETIME, dropofftime DATETIME, totalcost DECIMAL (6,2), active BOOLEAN,\
					googleEventId VARCHAR(30), PRIMARY KEY (bookingnumber), FOREIGN KEY (rego) REFERENCES car(rego), \
					FOREIGN KEY (email) REFERENCES user(email))")
	except pymysql.Error as e:
		print("Error 05: {}", e)

	print("Inserting")

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

		cur.execute("INSERT INTO user VALUES ('Johnno', 'John','Delaney','abc123','john@password.com') ")
		cur.execute("INSERT INTO user VALUES ('Fry', 'Philip','Fry','Leelha','fry@planetExpress.earth') ")

		cur.execute("INSERT INTO car VALUES ('XYZ987', 'Holden', 'Commodore',-37.799972,144.977393,'green')")
		cur.execute("INSERT INTO car VALUES ('ABC123', 'Holden', 'Commodore',-37.800633,144.979356,'blue')")
		cur.execute("INSERT INTO car VALUES ('U75PYV', 'Ford', 'Festiva',-37.801642,144.976127,'green')")
		cur.execute("INSERT INTO car VALUES ('YUPPIE', 'BMW', 'F32',-37.850139,144.997052,'silver')")
		cur.execute("INSERT INTO car VALUES ('AH786B', 'Toyota', 'Yaris',-37.859375,144.971699,'silver')")
		cur.execute("INSERT INTO car VALUES ('LMP675', 'Toyota', 'Camry',-37.856707,144.9678956,'blue')")
		cur.execute("INSERT INTO car VALUES ('XTK999', 'Ford', 'Falcon',-37.835074,144.9810364,'red')")
		cur.execute("INSERT INTO car VALUES ('GHR445', 'Toyota', 'Rav 4',-37.833413,144.982732,'silver')")

		pickup = datetime.datetime(2020,4,21,13)
		dropoff = pickup + timedelta(hours=4)
		cur.execute("INSERT INTO booking (rego, email, pickuptime, dropofftime, totalcost, active) VALUES\
					 ('XYZ987', 'john@password.com', '"+str(pickup)+"','"+str(dropoff)+"',60.00, 1)")

		pickup = datetime.datetime(2020,5,5,9)
		dropoff = pickup + timedelta(hours=6)
		cur.execute("INSERT INTO booking (rego, email, pickuptime, dropofftime, totalcost, active) VALUES\
					 ('U75PYV', 'john@password.com', '"+str(pickup)+"','"+str(dropoff)+"',42.00, 1)")

		pickup = datetime.datetime.now()
		pickup = pickup + timedelta(hours=-2)
		dropoff = pickup + timedelta(hours=4)
		cur.execute("INSERT INTO booking (rego, email, pickuptime, dropofftime, totalcost, active) VALUES\
					 ('U75PYV', 'fry@planetExpress.earth', '"+str(pickup)+"','"+str(dropoff)+"',42.00,1)")

		print("Inserted")

	except pymysql.Error as e:
		print("Error 06: {}", e)

	conn.commit()	

conn = db.get_connection()
clearDatabases(conn)
createTables(conn)



