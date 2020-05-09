import socket_utils as sockets

host = "192.168.3."
address = 63000

socket = sockets.sockets(host, address)

socket.send("Frank", "PooPoo")