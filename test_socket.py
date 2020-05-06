import unittest
import socket_utils as socket

class test_socket_utils:

	def __init__ (self):

		self.socket = socket.sockets()

	def test_listen(self):

		self.assertTrue(self.socket.listen() == "connected")


