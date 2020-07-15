import unittest
import AgentPi.agentpi as agent
import unittest.mock as mock
import socket

class test_agent_pi_utils(unittest.TestCase):

	def tearDown(self):
		agent.input = input

	def test_get_input(self):

		agent.input = lambda x: 'Geralt'
		self.assertTrue(agent.get_input("Please Enter Username: ") == "Geralt")

	def test_retrieve_password(self):

		name = 'Geralt'
		pswd = 'Witcher'
		hashed_pswd = '7e03a6c8ff248e1ecc9a94bc59ab37f26d7ed478a25fd4775473399599fe060b5ed442fd067ee3e31d3cfa78bd348e4d331b646364ac13ef96a83142b27e7effd91445035866a2776a0c6ec804e5c4f4bb3bcca2ca85ad4daa047540a658a8fc'
		self.assertTrue(agent.get_password(name, pswd) == hashed_pswd)

	def test_wrong_password(self):

		name = 'Geralt'
		pswd = 'Tiddly Winks'
		self.assertTrue(agent.get_password(name, pswd) == False)

	def test_non_password(self):

		client = None
		name = "Tommy Boy"
		pswd = "Julian"

		self.assertTrue(agent.getUser_remotely(name, pswd, client) == False)

	#These test the socket connections
	def test_socket(self):

		mock_socket = mock.Mock()
		mock_socket.recv.return_value = True

		#First tests a correct validation
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

		#Then we test a bad validation
		input("Press Enter")
		server_host = "192.168.3.6"
		port = 63000
		server_address = (server_host, port)
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(server_address)

		self.assertTrue(agent.getUser_remotely(name,pswd,client) == False)

		client.close()

		#We test that a car is returned successfully
		input("Press Enter")
		server_host = "192.168.3.6"
		port = 63000
		server_address = (server_host, port)
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(server_address)

		self.assertTrue(agent.returnCar(name, client) == True)

		#And a car returned unsuccessfully
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