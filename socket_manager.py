import socket_utils as sockets

host = ""
address = 63000
logout = False

socket = sockets.sockets(host, address)

while logout == False:
	print(socket.listen())
