#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import sys
sys.path.append('../')
sys.path.append('FacialRecognition')
import socket ,requests,json,socket_utils
import sqlite_utils as sqlite
import login,glob
import datetime
from getpass import getpass
from FacialRecognition.recognise import recognise


with open("../AgentPi/config.json", "r") as file:
    data = json.load(file)
    
HOST = data["masterpi_ip"] # The server's hostname or IP address.
PORT = 63000               # The port used by the server.
ADDRESS = (HOST, PORT)
DB = "../AgentPi/reception.db"
rego = data["rego"]

def main():
	unlocked = False
	operating = True

	try:
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print("Error creating socket: %s" % e)
		sys.exit(1)

	try:
		print("Connecting to {}...".format(ADDRESS))
		client.connect(ADDRESS)
		print("Connected.")
	except socket.gaierror as e:
		print("Address-related error connecting to server: %s" % e)
		sys.exit(1)

	while(operating == True):

		option = menu(unlocked)

		if option == "1":
            #Please do not remove the password function, for security I've used the getpass functionrather than get_input
			unlocked = getUser_remotely(get_input("Enter your email:\n"),getpass("Enter your Password:\n"),client)
			if unlocked == True:
				print("Bluetooth sent")
			else:
				print("Credentials were incorrect, please try again")

		elif(option == "2"):
			unlocked = recognise_face(unlocked)

			#facial recognition code here
		elif(option == "3"):

			user = returnCar(get_input("Enter your username:\n"),client)
			if(user == True):
				print("Car returned successfully")
				unlocked = False
			else:
				print("Username incorrect, please try again")
        
		elif(option == "0"):
			print("Goodbye.")
			print()
			operating = False
		else:
			print("Invalid input, try again.")
			print()

#Menu to enable user to chose which code to use
def menu(unlocked):

	valid_input = False

	while valid_input == False:

		if unlocked == False:
			print("1. Login via Console")
			print("2. Login via Facial Recognition")
		else:
			print("1. Return Car")

		print("0. Quit")
		print()

		text = input("Select an option: ")

		#Validates the input in restricting options
		if unlocked == False:

			if (text == "1") or (text == "2") or (text == "0"):

				valid_input = True

			else:
				print("Invalid Input")
		else:
			if text == "1":
				text = "3"
				valid_input = True
			elif text == "0":
				valid_input = True
			else:
				print("Invalid Input")

		print()

	return text   

#Source: https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
def get_input(input_type):

    entry = input(input_type)

    return entry

"""def get_password(user,password):

	db = sqlite.sqlite_utils(DB)
	stored_password = db.get_user(user)

	if len(stored_password)>0:
		stored_password = stored_password.pop()[0]
	else:
		stored_password = ""

	if (login.verify_password(stored_password, password)) == True:

		return stored_password

	else:

		return False"""

#Function that sends user details to the master pi for validation
def getUser_remotely(user,password,client):
    unlocked = False
    data={"email":user ,"password": password}
    url=("http://127.0.0.1:5000/hashme")
    password=requests.post(url, json=data)
    password=password.text
    password=password.replace("\n",'')
    password=password.replace('"','')
    print("Logging in as {}".format(user))
    print("hashed password : \""+password+"\"")
    socket_utils.sendJson(client,{"ForLogin": True,"ForReturnCar":False, "email":user,"password":password,"rego":rego,"date_time": str(datetime.datetime.now())})
    print("Waiting for Confirmation...")
    while(True):
        object = socket_utils.recvJson(client)
        if("Unlock" in object):
            print("Master Pi validated user, Unlock code to be sent from here to bluetooth device.")
            print()
            client.close()
            unlocked=True
            return unlocked
        else:
            print("Master Pi responded negative to unlock the car, again notify the user from here")
            return unlocked

#Fuction for facial recognition
def facialrecognition(img,client):
    print("In Facial recognition")
    name=recognise('encodings.pickle',img)
    user=name.split(":")
    unlocked=getUser_remotely(user[0],user[1],client)
    return unlocked

#Function that performs the return car function
def returnCar(username,client):
    print("Trying to return car for {}".format(username))
    socket_utils.sendJson(client, {"ForLogin": False,"ForReturnCar":True,"email": username, "rego": rego})
    print("Waiting for Confirmation...")
    while(True):
        object = socket_utils.recvJson(client)
        if("Return" in object):
            print("Car Return validated")
            print()
            client.close()
            return True
        else:
            print("Master Pi responded negative to unlock the car, again notify the user from here")
            client.close()
            return False

#Function to run the facial recognition
def recognise_face(unlocked, client):
	x=[f for f in glob.glob("*.png")]
	j=1
	for i in range(len(x)):
		print(j,x[i])
		j=j+1
		options=input("Select photo from uploaded photos")
		index=int(options)
		img=x[index-1]
		unlocked=facialrecognition(img,client)
		if unlocked==True:
			print("Bluetooth sent")
			return unlocked
		else:
			print("Unable to verify in master database, please try again")


# Execute program.
if __name__ == "__main__":
    main()
