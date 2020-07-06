"""
A test module for the day_modifiers class
"""
import unittest

from configuration import DayModifiers


class TestTimeSpent(unittest.TestCase):
    """
    Test class
    """

    def setUp(self):
        self.day_modifiers = DayModifiers()

    def test_instantiation(self):
        """
        Test instantiation of class with default variables
        and checks for expected values
        :return: None
        """
        min_time = 6
        avg_time = 25
        max_time = 75
        weekend_time = 60
        sunny_traffic_percent = 0.4
        sunny_chance_percent = 0.3
        sunny_time_spent = 15

        self.assertEqual(self.day_modifiers.min_time_spent, min_time)
        self.assertEqual(self.day_modifiers.avg_time_spent, avg_time)
        self.assertEqual(self.day_modifiers.max_time_spent, max_time)
        self.assertEqual(self.day_modifiers.weekend_time_spent, weekend_time)
        self.assertEqual(self.day_modifiers.sunny_time_spent, sunny_time_spent)
        self.assertEqual(self.day_modifiers.sunny_chance_percent, sunny_chance_percent)
        self.assertEqual(self.day_modifiers.sunny_traffic_percent, sunny_traffic_percent)

    def test_time_spent_weekday(self):
        """
        Test that time spent generated for a weekday is within bounds
        :return: None
        """

        min_time = self.day_modifiers.min_time_spent
        max_time = self.day_modifiers.max_time_spent

        for i in range(0, 50):
            self.assertGreaterEqual(max_time, self.day_modifiers.time_spent())
            self.assertLessEqual(min_time, self.day_modifiers.time_spent())
