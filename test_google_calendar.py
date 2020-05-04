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
		cal.insert(self.time_start, self.time_end, "XYZ123", "BMW", "X3", self.service)
		self.assertTrue(len(cal.get_events(self.service, 3)) == 1)
		self.assertTrue(cal.print_events(cal.get_events(self.service, 1)) == "2020-05-05T06:00:00+10:00 2020-05-05T07:00:00+10:00 Vehicle Booking XYZ123")
		#print("Hi")
		#print(cal.print_events(cal.get_events(self.service, 1)))

	def remove_event(self):
		print("Hi")

if __name__ == "__main__":
    unittest.main()