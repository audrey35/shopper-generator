from unittest import TestCase
from ShopperModel.Day import Day
from datetime import time

import pandas as pd


class TestDay(TestCase):

    def setUp(self):
        open_time = time(6, 0)
        close_time = time(21, 0)
        self.date = pd.to_datetime('today')
        self.test_day_class = Day(open_time, close_time, self.date, 100, 0.2)

    def test_create_shoppers(self):
        """
        Testing whether all the created shoppers have the same date as our Day class
        """
        self.test_day_class.create_shoppers(0.1, 0.1)
        test_shoppers = self.test_day_class.shoppers
        for shopper in test_shoppers:
            self.assertEqual(shopper.date, self.date)

    def test_shoppers_to_dict_no_shoppers(self):
        """
        If create_shoppers not called, a dictionary with no values is returned
        """
        test_dict = self.test_day_class.shoppers_to_dict();
        expected_dict = {'Date': [], 'DayOfWeek': [], 'TimeIn': [], 'TimeSpent': [], 'IsSenior': []}
        self.assertDictEqual(test_dict, expected_dict)
