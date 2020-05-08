import unittest
import socket_utils as sockets

class test_socket_utils(unittest.TestCase):

	host = ""
	address = 63000

	def setUp(self):

		self.socket = sockets.sockets(self.host, self.address)
		print(self.socket)

	def test_open_connection(self):

		print(self.socket.listen())

		#self.assertTrue(self.socket.listen() == "connected")

if __name__ == "__main__":
    unittest.main()
