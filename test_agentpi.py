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

	def test_get_user(self):

		#with mock.patch.object(__builtins__, 'input', lambda x: 'Geralt'):
		#	self.assertTrue(agent.console_login() == "car unlocked")

		#with mock.patch.object(__builtins__, 'input', lambda x: 'Geralt', lambda y: 'Winkler'):
		#	self.assertTrue(agent.console_login() == 'password incorrect')

		self.assertTrue(agent.console_login()=="Car Unlocked")
		self.assertTrue(agent.console_login()=="Password Incorrect")



if __name__ == "__main__":
    unittest.main()	