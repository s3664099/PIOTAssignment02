import bluetooth
import sqlite3 as lite

db_name = "engineer.db"

#The function takes a list of Json files that contains the name, and mac addresses
#The print statements exist to keep track of the movement of the function
def scan_devices(authorised_addresses):

	car_unlocked = False
	name = None
	print(authorised_addresses)

	while car_unlocked == False:

		#print("scanning")


		#Attempts to locate any nearby bluetooth devices
		nearby_devices = bluetooth.discover_devices()
		#print(nearby_devices)

		#Will then compare the nearby devices with the devices
		#In memorory
		for mac_address in nearby_devices:

			print(mac_address)
			print(bluetooth.lookup_name(mac_address, timeout=5))

			for addresses in authorised_addresses:

				#If there is a match, the vehicle will unlock
				if addresses['mac_address'] == mac_address:

					print("address found")
					car_unlocked == True
					name = addresses['name']
					
					return "Greetings {}. The car is unlocked".format(name)

def create_db():
	con = lite.connect(db_name)
	with con: 
		cur = con.cursor() 
		cur.execute("DROP TABLE IF EXISTS ENGINEER_data")
		cur.execute("CREATE TABLE ENGINEER_data(name VARCHAR, mac_address VARCHAR)")
		print("Database created")

	return con

def insert_engineer(con, name, mac_address):

	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO ENGINEER_data VALUES((?), (?))",(name, mac_address,))
		con.commit()
		return "Engineer details inserted"

def get_engineer(con):
	with con:
		engineer = con.execute("SELECT * FROM ENGINEER_data")
		engineers = []
		for x in engineer:
			engineers.append({'name': x[0], 'mac_address': x[1]})

		return engineers

def close_db(con):
	con.close()