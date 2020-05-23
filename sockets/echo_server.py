"""
.. module:: echo_server

"""
#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html
import socket
import socket_utils

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()
    waiting = True

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))

        while waiting == True:
            data = socket_utils.recvJson(conn)
            print(data)
            input("Press Enter")
            if(not data):
                break
            socket_utils.sendJson(conn , {"Unlock":"Unlock"})
            waiting = False
        
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")
