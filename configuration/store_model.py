"""
This module holds the domain model data for the store
"""
import calendar
from datetime import datetime

from shoppermodel.day import Day


class StoreModel:
    """
    Represents a grocery store
    """

    def __init__(self, lunch_rush, dinner_rush, holiday_modifiers, sunny_modifiers, senior_discount,
                 avg_shopper_traffic, open_time='06:00', close_time='21:00', percent_senior=0.2,
                 normal_min_time=6, normal_avg_time=25, normal_max_time=75):
        self.normal_avg_time = normal_avg_time
        self.normal_max_time = normal_max_time
        self.normal_min_time = normal_min_time
        self.lunch_rush = lunch_rush
        self.dinner_rush = dinner_rush
        self.sunny_modifiers = sunny_modifiers
        self.senior_discount = senior_discount
        self.holiday_modifiers = holiday_modifiers
        self.open_time = open_time
        self.close_time = close_time
        self.percent_senior = percent_senior
        self.avg_shopper_traffic = avg_shopper_traffic

    def create_day(self, date):
        """
        Creates a day
        :param date: the date to create a Day object for
        :return: a Day
        """
        day_name = calendar.day_name[date.weekday()]
        # get avg number of shoppers based on day of week
        num_of_shoppers = self.avg_shopper_traffic[day_name]
        # check if the date is a holiday
        num_of_shoppers = self.holiday_modifiers.apply_holiday_modifier(date, num_of_shoppers)
        return Day(self, num_of_shoppers, date)

    @property
    def open_time(self):
        """Return the open time."""
        return self._open_time

    @open_time.setter
    def open_time(self, open_time):
        """Set the open time."""
        try:
            open_time = datetime.strptime(open_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the open time because the provided open "
                                 "time ({}) is not a string in valid format"
                                 "(21:00).".format(open_time))

        try:
            if open_time < self._close_time:
                self._open_time = open_time
            else:
                raise ValueError("Invalid. Could not set the open time because the provided"
                                 "open time ({}) is greater than the close "
                                 "time({}).".format(open_time, self._close_time))
        except AttributeError:
            self._open_time = open_time

    @property
    def close_time(self):
        """Return the close time."""
        return self._close_time

    @close_time.setter
    def close_time(self, close_time):
        """Set the close time."""
        try:
            datetime.strptime(close_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the close time because the provided "
                                 "close time ({}) is not a string in valid format "
                                 "(21:00).".format(close_time))
        a_close_time = datetime.strptime(close_time, '%H:%M').time()
        try:
            if a_close_time > self._open_time:
                self._close_time = a_close_time
            else:
                raise ValueError("Invalid. Could not set the close time because the provided "
                                 "close time ({}) is less than the open "
                                 "time({}).".format(close_time, self._open_time))
        except AttributeError:
            self._close_time = a_close_time
