import random
from datetime import datetime


class Rush:
    """
    Class that represents a period of time in which customers will come into the store for a specific rush crowd.
    eg. a Lunch rush
    """

    def __init__(self, start_time, end_time, time_spent, percent):
        self.start_time = start_time
        self.end_time = end_time
        self.time_spent = time_spent
        self.percent = percent

    def percent_of(self, num):
        return round(self.percent * num)

    def calculate_time_spent(self, std=5):
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
            raise AttributeError("Invalid. Could not set the start time because the provided start time ({}) is"
                                 " not a string in valid format (21:00).".format(start_time))

        try:
            if start_time < self._end_time:
                self._start_time = start_time
            else:
                raise ValueError("Invalid. Could not set the start time because the provided start time ({}) is"
                                 " greater than the end time({}).".format(start_time, self._end_time))
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
            raise AttributeError("Invalid. Could not set the end time because the provided end time ({}) is"
                                 " not a string in valid format (21:00).".format(end_time))
        a_end_time = datetime.strptime(end_time, '%H:%M').time()
        try:
            if a_end_time > self._start_time:
                self._end_time = a_end_time
            else:
                raise ValueError("Invalid. Could not set the end time because the provided end time ({}) is"
                                 " less than the open time({}).".format(end_time, self._start_time))
        except AttributeError:
            self._end_time = a_end_time