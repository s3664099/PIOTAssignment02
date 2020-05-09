import socket, json, sys
import struct

sys.path.append("..")

#Sets up the class for the socket
class sockets:

	HOST = ""    	# Empty string means to listen on all IP's on the machine, also works with IPv6.
             		# Note "0.0.0.0" also works but only with IPv4.
	PORT = 0	 	# Port to listen on (non-privileged ports are > 1023).
	ADDRESS = (HOST, PORT)
	s = None

	def __init__ (self, host, port):

		self.HOST = host
		self.PORT = port
		self.ADDRESS = (host, port)

	#Listens to socket for incoming message
	def listen(self):

		#Opens the socket and listes
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind(self.ADDRESS)
			s.listen()

			connected = False

			#Loop waiting for a message to be recieved
			while connected == False:
				print("Waiting")
				conn, address = s.accept()

				#When message is recieved it is set to be decoded
				message = self.recvJson(conn)

				#Once message is recieved, breaks out of it
				with conn:
					connected = True

			#Closes the socket
			s.shutdown(socket.SHUT_RDWR)
			s.close()

			return message

	#Function to send a message
	def send(self, username, password):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

			#Attempt to connect 
			print("Connecting to {}...".format(self.ADDRESS))
			s.connect(self.ADDRESS)
			print("Connected.")

			print("Logging in as {}".format(username))

			#Encodes the message and sends it to the other socket
			self.sendJson(s, {"username": username, "password": password})

			s.shutdown(socket.SHUT_RDWR)
			s.close()



	#Takes the message recieved by the system and converts it into JSON format
	def recvJson(self, socket):
		buffer = socket.recv(4)
		jsonLength = struct.unpack("!i", buffer)[0]

		# Reference: https://stackoverflow.com/a/15964489/9798310
		buffer = bytearray(jsonLength)
		view = memoryview(buffer)
		while jsonLength:
			nbytes = socket.recv_into(view, jsonLength)
			view = view[nbytes:]
			jsonLength -= nbytes

		#Decodes the message and returns it as a Json object
		jsonString = buffer.decode("utf-8")
		return json.loads(jsonString)

	#Encodes the message and sends it across the socket
	def sendJson(socket, object):
		jsonString = json.dumps(object)
		data = jsonString.encode("utf-8")
		jsonLength = struct.pack("!i", len(data))
		socket.sendall(jsonLength)
		socket.sendall(data)
