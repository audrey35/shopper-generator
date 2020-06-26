"""
test modules
"""
import unittest
from Configuration.rush import Rush


class TestTimeSpent(unittest.TestCase):
    """
    Test class for time_spent.py
    """

    def test_time_spent(self):
        """
        Test instantiation of class and checks for expected times
        :return: None
        """
        expected_avg_time = 15
        rush = Rush("14:00", "15:00", 20, 0.2, 6, 75, 15)
        self.assertEqual(expected_avg_time, rush.normal_avg_time)
