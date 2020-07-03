"""
Tests for the holiday modifiers class
"""
from unittest import TestCase
from datetime import date, timedelta
from configuration import HolidayModifiers


class TestHolidayModifiers(TestCase):
    """
    Test class for the holiday_modifiers.py
    """

    def setUp(self):
        self.holiday_modifiers = HolidayModifiers()
        self.num_of_shoppers = 1000

    def test_apply_holiday_modifier(self):
        """
        Test whether the each type of holiday modifier is applied correctly
        """
        holiday_percent = self.holiday_modifiers.holiday_percent
        day_before_percent = self.holiday_modifiers.day_before_percent
        week_before_percent = self.holiday_modifiers.week_before_percent
        expected_if_holiday = round(self.num_of_shoppers * holiday_percent)
        expected_if_day_before = round(self.num_of_shoppers * (1 + day_before_percent))
        expected_if_week_before = round(self.num_of_shoppers * (1 + week_before_percent))

        time_delta = timedelta(days=1)
        holiday = date.fromisoformat("2020-10-12")
        day_before = holiday - time_delta
        week_before = [holiday - 2 * time_delta,
                       holiday - 3 * time_delta,
                       holiday - 4 * time_delta,
                       holiday - 5 * time_delta,
                       holiday - 6 * time_delta]

        self.assertEqual(expected_if_holiday,
                         self.holiday_modifiers
                         .apply_holiday_modifier(holiday, self.num_of_shoppers))
        self.assertEqual(expected_if_day_before,
                         self.holiday_modifiers
                         .apply_holiday_modifier(day_before, self.num_of_shoppers))
        for date_in_week in week_before:
            self.assertEqual(expected_if_week_before,
                             self.holiday_modifiers
                             .apply_holiday_modifier(date_in_week, self.num_of_shoppers))

    def test_non_holiday(self):
        """
        Test that there is no change to number of shoppers when date is not a holiday
        """
        test_date = date.fromisoformat("2020-01-02")
        self.assertFalse(test_date in self.holiday_modifiers.holidays)
        self.assertEqual(self.num_of_shoppers,
                         self.holiday_modifiers
                         .apply_holiday_modifier(test_date, self.num_of_shoppers))
