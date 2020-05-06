import socket, json, sys
sys.path.append("..")
import socket_utils

class sockets:

	HOST = ""    	# Empty string means to listen on all IP's on the machine, also works with IPv6.
             		# Note "0.0.0.0" also works but only with IPv4.
	PORT = 63000 	# Port to listen on (non-privileged ports are > 1023).
	ADDRESS = (HOST, PORT)

	def __init__ (self):
	    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	        s.bind(self.ADDRESS)
	        s.listen()

	def listen(self):

		connected = False

		print("Listening on {}...".format(ADDRESS))
		while connected = False:
			print("Waiting")
			conn, address = s.accept()

			with conn:
				connected = True

		return "connected"
