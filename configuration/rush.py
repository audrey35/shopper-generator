"""
Represents a period of time in which customers will come into
the store for a specific rush crowd. eg. a Lunch rush
"""
import random
from datetime import datetime


class Rush:
    """
    Class that represents a period of time in which customers will come into
    the store for a specific rush crowd. eg. a Lunch rush
    """

    def __init__(self, start_time, end_time, time_spent, percent):
        """
        Initializes Rush.
        :param start_time: rush start time as a military time string.
        :param end_time: rush end time as a military time string.
        :param time_spent: average time a shopper spends during the rush.
        :param percent: percent increase in number of shoppers during the rush as a decimal.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.time_spent = time_spent
        self.percent = percent

    def percent_of(self, num):
        """
        Returns percent of a given number.
        :param num: an integer.
        :return: calculated percent of the given number rounded to an integer.
        """
        return round(self.percent * num)

    def calculate_time_spent(self, std=5):
        """
        Returns a randomly generated integer for time spent.
        :param std: standard deviation to be applied.
        :return: a randomly generated integer for time spent.
        """
        return round(random.gauss(self.time_spent, std))

    @property
    def start_time(self):
        """Return the start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Set the start time."""
        try:
            start_time = datetime.strptime(start_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the start time because the provided start time"
            msg += " ({}) is not a string in valid format (21:00).".format(start_time)
            raise AttributeError(msg)

        try:
            if start_time < self._end_time:
                self._start_time = start_time
            else:
                msg = "Invalid. Could not set the start time because the provided start time"
                msg += " ({}) is greater than the end time({}).".format(start_time, self._end_time)
                raise ValueError(msg)
        except AttributeError:
            self._start_time = start_time

    @property
    def end_time(self):
        """Return the end time."""
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Set the end time."""
        try:
            datetime.strptime(end_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the end time because the provided end time "
            msg += "({}) is not a string in valid format (21:00).".format(end_time)
            raise AttributeError(msg)
        a_end_time = datetime.strptime(end_time, '%H:%M').time()
        try:
            if a_end_time > self._start_time:
                self._end_time = a_end_time
            else:
                msg = "Invalid. Could not set the end time because the provided end time "
                msg += "({}) is less than the open time({}).".format(end_time, self._start_time)
                raise ValueError(msg)
        except AttributeError:
            self._end_time = a_end_time
