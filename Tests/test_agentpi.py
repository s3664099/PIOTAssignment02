import sys
sys.path.append('../')
sys.path.append('../AgentPi')

import unittest
import mock
import agentpi as agent

class test_agent_pi_utils(unittest.TestCase):

	def tearDown(self):
		agent.input = input

	def test_login_locally(self):
		self.assertTrue(agent.getUser_locally('Geralt','Witcher')==1)
		self.assertTrue(agent.getUser_locally('geralt@rivia.net','Witcher')==1)
		self.assertTrue(agent.getUser_locally('Geralt','willy')==2)
		self.assertTrue(agent.getUser_locally('Milly','Milkshake')==0)

	def test_get_input(self):

		agent.input = lambda x: 'Geralt'
		self.assertTrue(agent.get_input("Please Enter Username: ") == "Geralt")

	def test_console_login(self):

		name = 'Geralt'
		pswd = 'Witcher'
		bad_pswd = 'willy'

		self.assertTrue(agent.console_login(name, pswd)=="Car Unlocked")
		self.assertTrue(agent.console_login(name, bad_pswd)=="Password Incorrect")



if __name__ == "__main__":
    unittest.main()	