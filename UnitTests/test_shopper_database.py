"""Tests the ShopperDatabase class."""

from unittest import TestCase

from ShopperDatabase import ShopperDatabase
from ShopperModel import Configuration


class TestShopperDatabase(TestCase):
    """
    Tests the ShopperDatabase class.
    """

    def setUp(self):
        self.configuration = Configuration(start_date="2018-01-01", end_date="2019-12-31",
                                           open_time="06:00", close_time="21:00",
                                           mon_avg_traffic=800, tues_avg_traffic=1000,
                                           wed_avg_traffic=1200,
                                           thurs_avg_traffic=900, fri_avg_traffic=2500,
                                           sat_avg_traffic=4000, sun_avg_traffic=5000,
                                           lunchtime_percent=0.05, dinnertime_percent=0.05,
                                           senior_percent=0.2, senior_discount_percent=0.5,
                                           min_time_spent=6, avg_time_spent=25, max_time_spent=75,
                                           lunch_avg_time_spent=10, dinner_avg_time_spent=20,
                                           weekend_avg_time_spent=60,
                                           sunny_weekend_avg_time_spent=10,
                                           senior_min_time_spent=45, senior_max_time_spent=60)
        self.shopper_database = ShopperDatabase(self.configuration)

    def test_valid_creation(self):
        """
        Tests valid creation of ShopperDatabase object.
        """
        self.assertEqual(self.shopper_database.collection, None, "Should be None")
        self.assertEqual(self.shopper_database.database, None, "Should be None")
        self.assertEqual(self.shopper_database.configuration, self.configuration,
                         "Should be identical")

    def test_invalid_creation(self):
        """
        Tests TypeError is raised if invalid parameter is passed to ShopperDatabase.
        """
        with self.assertRaises(TypeError):
            ShopperDatabase(5)

    def test_populate_shopper_database(self):
        """
        Tests populate_populate_shopper_database method works as expected.
        """
        # create ShopperTable before testing
