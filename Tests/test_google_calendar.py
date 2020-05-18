import sys
sys.path.append('../')
sys.path.append('../Database')

import unittest
from datetime import datetime
from datetime import timedelta
import gcalendar_utils as cal

class test_database_utils(unittest.TestCase):

	def setUp(self):
		date = datetime.now()
		tomorrow = (date + timedelta(days = 1)).strftime("%Y-%m-%d")
		self.time_start = "{}T06:00:00+10:00".format(tomorrow)
		self.time_end = "{}T07:00:00+10:00".format(tomorrow)
		self.service = cal.connect_calendar()

	def test_add_event(self):
		GoogleId = cal.insert(self.time_start, self.time_end, "XYZ123", "BMW", "X3", "36.00", "dasarkies@gmail.com",self.service)
		self.assertTrue(len(cal.get_events(self.service, 3)) == 1)
		self.assertTrue(cal.print_events(cal.get_events(self.service, 1)) == self.time_start+" "+self.time_end+" Vehicle Booking XYZ123")
		cal.remove_event(GoogleId, self.service)
		self.assertTrue(len(cal.get_events(self.service, 3)) == 0)



if __name__ == "__main__":
    unittest.main()