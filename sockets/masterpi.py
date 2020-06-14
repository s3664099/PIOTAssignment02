"""
.. module:: masterpi

"""
#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket
import sys

import requests
import threading

import socket_utils


class ClientThread(threading.Thread):
    """
    Client threading

    """
    def __init__(self,clientAddress,clientsocket):
        """
        Add connection

        """
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddr=clientAddress
        print ("New connection added: ", self.caddr)
    def run(self):
        """
        Receive connection from server

        """
        print ("Connection from : ", self.caddr)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while(True):
            data= socket_utils.recvJson(self.csocket)

            if ("ForService" in data):
                if(data["Check_Status"] == True):

                    url = ("http://127.0.0.1:5000/getservicestatus/"+data["rego"])
                    response = requests.get(url)
                    respond = response.text
                    response = response.json()

                    if "request_no" in respond:
                        socket_utils.sendJson(self.csocket, {"service_no": response})
                    else:
                        socket_utils.sendJson(self.csocket, {"Response": "No Service"})
                else:
                    url = ("http://127.0.0.1:5000/updateservicestatus/"+str(data["service_no"]))
                    response = requests.post(url)
                    
                    socket_utils.sendJson(self.csocket, {"Response": response.text})

            elif("ForLogin" in data):
                if(data["ForLogin"]==True):

                    if(data["ForBlueTooth"]==True):

                        url = ("http://127.0.0.1:5000/getengineerbluetoothdetails")
                        response = requests.get(url)
                        respond = response.text
                        response = response.json()

                        if "firstname" in respond:
                            socket_utils.sendJson(self.csocket, {"Engineers": response})
                        else:
                            socket_utils.sendJson(self.csocket, {"Response": "Failure"})
                        
                    elif(data["ForQRCode"] == True):

                        data["first_name"] = data["first_name"].replace(',','')
                        data["surname"] = data["surname"].replace(',','')

                        url = ("http://127.0.0.1:5000/finduserdetails/"+data["email"])
                        response = requests.get(url)
                        respond = response.text

                        if "firstname" in respond:

                            response = response.json().pop()

                            if (response["firstname"] == data["first_name"]) and (response["lastname"] == data["surname"]):
                                socket_utils.sendJson(self.csocket, {"Unlock": True})

                        socket_utils.sendJson(self.csocket, {"Response": 'QR code invalid'})

                    elif(data["FacialRecognition"]==False):
                        url=("http://127.0.0.1:5000/validate")
                        response=requests.post(url,json=data)
                        response=response.text
                        if response:
                            response=response.replace('"','')
                            response=response.replace('\n','')
                        if "Success" in response:
                                url=("http://127.0.0.1:5000/updatecarstatus")
                                car={"rego" :data['rego']}
                                response=requests.post(url,json=car)
                                response=response.text
                                if response=="Success":
                                    socket_utils.sendJson(self.csocket , { "Unlock": True })
                                else:
                                    socket_utils.sendJson(self.csocket, {"Lock" : True, "Response" : 'Unable to update car status, please try later'})
                        elif response=="Car Already Unlocked":
                                socket_utils.sendJson(self.csocket, {"Unlock" : True, "Response" : 'Car Already Unlocked'})
                                
                        elif "Booking Not Found" in response:
                                socket_utils.sendJson(self.csocket , { "Lock": True,"Response" : 'Booking not found' })

                        else:
                                socket_utils.sendJson(self.csocket , { "Lock": True,"Response" : 'Credentials not found, please check and try again' })
                    elif (data["FacialRecognition"]==True):
                        url=("http://127.0.0.1:5000/validateUser")
                        response=requests.post(url,json=data)
                        response=response.text
                        if response:
                            response=response.replace('"','')
                            response=response.replace('\n','')
                        if "Success" in response:
                                url=("http://127.0.0.1:5000/updatecarstatus")
                                car={"rego" :data['rego']}
                                response=requests.post(url,json=car)
                                response=response.text
                                if response=="Success":
                                    socket_utils.sendJson(self.csocket , { "Unlock": True })
                                else:
                                    socket_utils.sendJson(self.csocket, {"Lock" : True, "Response" : 'Unable to update car status, please try later'})
                        elif response=="Car Already Unlocked":
                                socket_utils.sendJson(self.csocket, {"Unlock" : True, "Response" : 'Car Already Unlocked'})
                                
                        elif "Booking Not Found" in response:
                                socket_utils.sendJson(self.csocket , { "Lock": True,"Response" : 'Booking not found' })

                        else:
                                socket_utils.sendJson(self.csocket , { "Lock": True,"Response" : 'Credentials not found, please check and try again' })


                elif (data["ForReturnCar"]==True):
                    url=("http://127.0.0.1:5000/returncar")
                    response=requests.post(url, json=data)
                    response=response.text
                    if response:
                        response=response.replace('"','')
                        response=response.replace('\n','')
                        socket_utils.sendJson(self.csocket,{"Response": response})
            elif (data["Quit"]==True):
                self.csocket.close()
                break


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
    """
    Start connection

    """
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
