"""
.. module:: agentpi

"""
#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import sys
import socket ,requests,json, agent_socket_utils
from google.cloud import storage
import glob
import datetime
from getpass import getpass
from FacialRecognition.recognise import recognise


with open("config.json", "r") as file:
	
    data = json.load(file)
    
HOST = data["masterpi_ip"] # The server's hostname or IP address.
PORT = 63000               # The port used by the server.
ADDRESS = (HOST, PORT)
rego = data["rego"]

def main():
	"""
	Connection to server

	"""
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
		"""
		Options menu

		"""
		option = menu(unlocked)

		if option == "1":
            #Please do not remove the password function, for security I've used the getpass functionrather than get_input
			unlocked = getUser_remotely(get_input("Enter your email:\n"),getpass("Enter your Password:\n"),client)
			if unlocked == True:
				print("Bluetooth sent")
			else:
				print("please try again")

		elif(option == "2"):
			unlocked = recognise_face(unlocked,client)

			#facial recognition code here
		elif(option == "3"):

			user = returnCar(get_input("Enter your username:\n"),client)
			if(user == True):
				print("Car returned successfully")
				unlocked = False
			else:
				print("Username incorrect, please try again")
        
		elif(option == "0"):
			data={"Quit": True}
			agent_socket_utils.sendJson(client,data)
			print("Goodbye.")
			print()
			operating = False
			client.close()
		else:
			print("Invalid input, try again.")
			print()

#Downloads the encodings.pickle file from Cloud Storage for Facial Recognition
def download_blob():
        """
		Downloads a blob from the bucket.
		
		"""
        bucket_name = "car-hire"
        source_blob_name = "encodings.pickle"
        destination_file_name = "FacialRecognition/encodings.pickle"

        storage_client = storage.Client() 
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

#Menu to enable user to chose which code to use
def menu(unlocked):
	"""
	Menu for user to login through via console or facial recognition
	
	"""
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
	"""
	Get input call

	"""
    entry = input(input_type)

    return entry

#Function that sends user details to the master pi for validation
def getUser_remotely(user,password,client):
	"""
	Send user details to the master pi

	"""
	unlocked = False
	data={"email":user ,"password": password}
	#Change the URL based on the location at which the API is hosted
	url=("http://127.0.0.1:5000/hashme")
	password=requests.post(url, json=data)
	password=password.text
	password=password.replace("\n",'')
	password=password.replace('"','')
	print("Logging in as {}".format(user))
	agent_socket_utils.sendJson(client,{"FacialRecognition": False,"ForLogin": True,"ForReturnCar":False, "email":user,"password":password,"rego":rego,"date_time": str(datetime.datetime.now())})
	print("Waiting for Confirmation...")
	while(True):
		object = agent_socket_utils.recvJson(client)
		if("Unlock" in object):
			if("Response" in object):
				print(object['Response'])
				return True
			else:
				print()
			print("Master Pi validated user, Unlock code to be sent from here to bluetooth device.")
			print()
			unlocked=True
			return unlocked
		else:
			print(object['Response'])
			return unlocked

def getUserName_remotely(username,client):
	"""
	Get username remotely

	"""
	unlocked=False
	print("Logging in as {}".format(username))
	agent_socket_utils.sendJson(client,{"FacialRecognition": True, "ForLogin": True,"ForReturnCar":False, "email":username,"rego":rego,"date_time": str(datetime.datetime.now())})
	print("Waiting for Confirmation...")
	while(True):
		object = agent_socket_utils.recvJson(client)
		if("Unlock" in object):
			if("Response" in object):
				print(object['Response'])
				return True
			else:
				print()
			print("Master Pi validated user, Unlock code to be sent from here to bluetooth device.")
			print()
			unlocked=True
			return unlocked
		else:
			print(object['Response'])
			return unlocked


#Fuction for facial recognition
def facialrecognition(img,client):
	"""
	Facial recognition function

	"""
	print("In Facial recognition")
	download_blob()
	name=recognise('FacialRecognition/encodings.pickle',img)
    #user=name.split(":")
	unlocked=getUserName_remotely(name,client)
	return unlocked

#Function that performs the return car function
def returnCar(username,client):
	"""
	Return car function

	"""
    print("Trying to return car for {}".format(username))
    agent_socket_utils.sendJson(client, {"ForLogin": False,"ForReturnCar":True,"email": username, "rego": rego})
    print("Waiting for Confirmation...")
    while(True):
        object = agent_socket_utils.recvJson(client)
        if(object['Response']=="Success"):
            print("Car Returned successfully, thank you for using our services")
            print()
            return True
        else:
            print(object['Response'])
            return False

#Function to run the facial recognition
def recognise_face(unlocked, client):
	"""
	Facial recognition to run facial recognization

	"""
	x=[f for f in glob.glob("Images/*.png")]
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
		return False

# Execute program.
if __name__ == "__main__":
    main()
