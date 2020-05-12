#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
from flask import Flask, request, jsonify
import socket, json, sys
sys.path.append("..")
import socket_utils
import requests, threading,time


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddr=clientAddress
        print ("New connection added: ", self.caddr)
    def run(self):
        print ("Connection from : ", self.caddr)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while(True):
            data= socket_utils.recvJson(self.csocket)
            url=("http://127.0.0.1:5000/validate")
            response=requests.post(url,json=data)
            response=response.text
            if response:
                response=response.strip("\"")
                response=response.strip("\"")
            if "Success" in response:    
                    socket_utils.sendJson(self.csocket , { "Unlock": True })
                    self.csocket.close()
                    break
            elif "Booking Not Found" in response:
                    socket_utils.sendJson(self.csocket , { "Unlock": True })
                    self.csocket.close()
                    break
            else:
                    socket_utils.sendJson(self.csocket , { "Lock": True })
                
            """login=json.loads(response.text)

            if(login=="Success"):  
                socket_utils.sendJson(self.csocket , { "Unlock": True })
                self.csocket.close()
                break
            else:
             socket_utils.sendJson(self.csocket , { "Lock": True })"""



HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Error creating socket: %s" % e)
    sys.exit(1)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started")
while True:
    server.listen()
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()




def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()
        while True:
            conn, addr = s.accept()
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()

                

     

# Execute program.
if __name__ == "__main__":
    main()