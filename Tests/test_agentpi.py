import sys
sys.path.append('../')
sys.path.append('../AgentPi')

import unittest
import agentpi as agent
import mock
import socket

class test_agent_pi_utils(unittest.TestCase):

	def tearDown(self):
		agent.input = input

	def test_get_input(self):

		agent.input = lambda x: 'Geralt'
		self.assertTrue(agent.get_input("Please Enter Username: ") == "Geralt")

	def test_retrieve_password(self):

		name = 'Tommy Boy'
		pswd = 'Witcher'

		self.assertTrue(agent.get_password(name, pswd) == 'Witcher')

		name = 'Geralt'
		pswd = 'Witcher'
		hashed_pswd = '5ed442fd067ee3e31d3cfa78bd348e4d331b646364ac13ef96a83142b27e7effd91445035866a2776a0c6ec804e5c4f4bb3bcca2ca85ad4daa047540a658a8fc'
		self.assertTrue(agent.get_password(name, pswd) == hashed_pswd)

	def test_non_password(self):

		client = None
		name = "Tommy Boy"
		pswd = "Julian"

		self.assertTrue(agent.getUser_remotely(name, pswd, client) == False)

	def test_socket(self):

		mock_socket = mock.Mock()
		mock_socket.recv.return_value = True

		input("Press Enter")
		server_host = "192.168.3.6"
		port = 63000
		server_address = (server_host, port)
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(server_address)

		name = 'Geralt'
		pswd = 'Witcher'

		self.assertTrue(agent.getUser_remotely(name,pswd,client) == True)



		client.close()

		input("Press Enter")
		server_host = "192.168.3.6"
		port = 63000
		server_address = (server_host, port)
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(server_address)

		self.assertTrue(agent.getUser_remotely(name,pswd,client) == False)

		client.close()

		input("Press Enter")
		server_host = "192.168.3.6"
		port = 63000
		server_address = (server_host, port)
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(server_address)

		self.assertTrue(agent.returnCar(name, client) == True)

		input("Press Enter")
		server_host = "192.168.3.6"
		port = 63000
		server_address = (server_host, port)
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(server_address)

		self.assertTrue(agent.returnCar(name, client) == False)




"""
	def test_input(self):

		agent.menu(False)
		agent.menu(True)
"""


if __name__ == "__main__":
    unittest.main()	