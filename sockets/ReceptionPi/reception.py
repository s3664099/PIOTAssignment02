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
    while(True):
        print("1. Login as mbolger")
        print("2. Login as shekhar")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):
            user = getUser("mbolger")
            login(user)
        elif(text == "2"):
            user = getUser("shekhar")
            login(user)
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

def login(user):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        print("Logging in as {}".format(user["username"]))
        socket_utils.sendJson(s, user)

        print("Waiting for Master Pi...")
        while(True):
            object = socket_utils.recvJson(s)
            if("logout" in object):
                print("Master Pi logged out.")
                print()
                break

# Execute program.
if __name__ == "__main__":
    main()
