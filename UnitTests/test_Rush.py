from unittest import TestCase
from datetime import time

from configuration.Rush import Rush


class TestRush(TestCase):
    """
    Test class for the Rush class
    """

    def test_rush_creation(self):
        """
        Test instantiation. Checks if the instance variables are of correct type. Testing for the following user story:
        As the technical user, I can modify when the lunch or dinner rush happens during the day.
        """
        rush = Rush("12:00", "13:00", 10, 0.2)
        expected_start_time = time.fromisoformat("12:00")
        expected_end_time = time.fromisoformat("13:00")
        expected_time_spent = 10
        expected_percent = 0.2

        self.assertIsInstance(rush.start_time, time)
        self.assertIsInstance(rush.end_time, time)
        self.assertEqual(expected_start_time, rush.start_time)
        self.assertEqual(expected_end_time, rush.end_time)
        self.assertEqual(expected_time_spent, rush.time_spent)
        self.assertEqual(expected_percent, rush.percent)

    # def test_rush_creation_error(self):
    #     """
    #     Test instantiation when the start and end times are before and after each other respectively
    #     """
    #     self.assertRaises(ValueError, Rush("12:00", "10:00", 10, 0.2))


