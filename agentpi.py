#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket 
import json
import sys
sys.path.append("..")
import socket_utils
import sqlite_utils as sqlite
import login,glob
from getpass import getpass
from FacialRecognition.recognise import recognise


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
            username=input("Enter your email :")
            password = getpass()
            #result= console_login(username,password)

            #if "Unlocked" in result:
            verification=getUser_remotely(username,password,client)
            if verification==True:
                    #bluetooth code
                break
            else:
                    print("Unable to verify in master database, please try again")
            #else:
             #   print("Credentials were incorrect, please try again")

        elif(text == "2"):
            x=[f for f in glob.glob("*.png")]
            j=1
            for i in range(len(x)):
                print(j,x[i])
                j=j+1
            options=input("Select photo from uploaded photos")
            index=int(options)
            img=x[index-1]
            verification=facialrecognition(img,client)
            if verification==True:
                    #bluetooth code
                break
            else:
                    print("Unable to verify in master database, please try again")
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

#    else:
        #Otherwise checks remotely
 #       user = getUser_remotely(username)

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


def getUser_remotely(user,password,client):
    unlocked=False
    print("Logging in as {}".format(user))
    socket_utils.sendJson(client,{"email":user,"password":password,"rego":rego})
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


def facialrecognition(img,client):
    print("In Facial recognition")
    name=recognise('encodings.pickle',img)
    user=name.split(":")
    unlocked=getUser_remotely(user[0],user[1],client)
    return unlocked

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
