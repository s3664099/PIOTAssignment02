#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sqlite3, sys
sys.path.append("..")
import socket_utils

DB_NAME = "reception.db"

with open("config.json", "r") as file:
    data = json.load(file)
    
HOST = data["masterpi_ip"] # The server's hostname or IP address.
PORT = 63000               # The port used by the server.
ADDRESS = (HOST, PORT)

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

    while(True):
        print("1. Login via Console")
        print("2. Login via Facial Recognition")
        print("3. Return Car")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):
            username= input("Enter your username:\n")
            user=getUser(username)
            unlocked=login(user,client)
            if(unlocked==True):
                #bluetooth and pushbullet code here
                break
        elif(text == "2"):
            facialrecognition()
            #facial recognition code here
        elif(text == "3"):
            username= input("Enter your username:\n")
            user=returnCar(username,client)
            if(user==True):
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

def getUser(username):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    with connection:
        cursor = connection.cursor()
        cursor.execute("select * from Users where UserName = ?", (username,))
        row = cursor.fetchone()
    connection.close()

    return { "username": row["UserName"], "firstname": row["FirstName"], "lastname": row["LastName"]  }

def login(user,client):
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
