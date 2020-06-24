"""
test module
"""
from unittest import TestCase
from datetime import time
from Configuration.senior_discount import SeniorDiscount


class TestSeniorDiscount(TestCase):
    """
    Test class for senior_discount.py
    """

    def test_senior_discount(self):
        """
        Test instantiation of object
        :return: None
        """
        start_time = time.fromisoformat("1400")
        end_time = time.fromisoformat("1600")
        min_time = 10
        max_time = 60
        percent = 20
        expected_min_time = 10
        expected_percent = 20
        senior_discount = SeniorDiscount(start_time, end_time, min_time, max_time, percent)
        self.assertEqual(expected_min_time, senior_discount.min_time_spent)
        self.assertEqual(expected_percent, senior_discount.percent)
