"""
This module holds the domain model data for the store
"""
import calendar
from datetime import datetime

from ShopperModel.day import Day


class StoreModel:
    """
    Represents a grocery store
    """

    def __init__(self, lunch_rush, dinner_rush, holiday_modifiers, sunny_modifiers, senior_discount,
                 open_time='06:00', close_time='21:00', percent_senior=0.2):
        self.lunch_rush = lunch_rush
        self.dinner_rush = dinner_rush
        self.sunny_modifiers = sunny_modifiers
        self.senior_discount = senior_discount
        self.holiday_modifiers = holiday_modifiers
        self.open_time = open_time
        self.close_time = close_time
        self.percent_senior = percent_senior
        self.days_of_week = {'Monday': None, 'Tuesday': None, 'Wednesday': None, 'Thursday': None,
                             'Friday': None, 'Saturday': None, 'Sunday': None}

    def add_day_of_week(self, day_of_week):
        """
        Adds a day of week to the grocery store
        :param day_of_week: a day of week object
        :return: None
        """
        if self.days_of_week[day_of_week.day_name] is None:
            self.days_of_week[day_of_week.day_name] = day_of_week
        else:
            raise ValueError('The day of week ' + day_of_week.day_name + ' is already defined')

    def create_day(self, date):
        """
        Creates a day
        :param date: the date to create a Day object for
        :return: a Day
        """
        day_name = calendar.day_name[date.weekday()]
        # get avg number of shoppers based on day of week
        num_of_shoppers = self.days_of_week[day_name].shopper_traffic
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
