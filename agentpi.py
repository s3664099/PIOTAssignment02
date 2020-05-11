#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket 
import json
import sys
sys.path.append("..")
import socket_utils
import sqlite_utils as sqlite
import login

with open("config.json", "r") as file:
    data = json.load(file)
    
HOST = data["masterpi_ip"] # The server's hostname or IP address.
PORT = 63000               # The port used by the server.
ADDRESS = (HOST, PORT)
DB = "reception.db"
operating = True
unlocked = False
rego = data["rego"]

def main():
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
        print("1. Login via Console")
        print("2. Login via Facial Recognition")
        print("3. Return Car")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):

            if (unlocked == True):
                print("Car already unlocked")

            print(console_login(get_input("Enter your username:\n"),get_input("Enter your password:\n")))

        elif(text == "2"):
            facialrecognition()
            #facial recognition code here
        elif(text == "3"):
            username = input("Enter your username:\n")
            user=returnCar(username,client)
            if(user == True):
                print("Car returned successfully")
            else:
                print("Username incorrect, please try again")
        
        elif(text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()

#This function handles the console login part
def console_login(username, password):

    #checks to see if it is stored locally, and password is correct
    user=getUser_locally(username, password)

    if (user == 1):

        return("Car Unlocked")

    elif (user == 2):
        return("Password Incorrect")

    else:
        #Otherwise checks remotely
        user = getUser_remotely(username,password)

#Source: https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
def get_input(input_type):

    entry = input(input_type)

    return entry

#This function checks to see if the user has been stored locally
#in the sqlite database. If it is, the passwords are compared.
def getUser_locally(username,password):

    #Default no user is present
    verified_user = 0

    #credentials obtained fro the database
    db = sqlite.sqlite_utils(DB)
    credentials = db.get_user(username)

    if len(credentials) > 0:

        #The credentials are compared with the hashing function
        #And returned based on validity or not
        credentials = credentials.pop()
        if (login.verify_password(credentials[1], password)) == True:
            verified_user = 1
        else:
            verified_user = 2

    return verified_user


def getUser_remotely(user,client):
    unlocked=False
    print("Logging in as {}".format(user["username"]))
    socket_utils.sendJson(client, user)
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


def facialrecognition():
    print("In Facial recognition")
    return

def returnCar(username,client):
    print("Trying to return car for {}".format(username["username"]))
    socket_utils.sendJson(client, username)
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



# Execute program.
if __name__ == "__main__":
    main()
