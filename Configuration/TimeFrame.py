import holidays
import pandas as pd

from datetime import datetime


class TimeFrame:
    """
    The TimeFrame represents the time period for the shopper behavior being tracked.
    It knows whether a date is a holiday and can create a list of dates within the time period.
    """
    holidays = holidays.US()

    def __init__(self, start_date="2020-01-01", end_date="2020-12-31"):
        self.start_date = start_date
        self.end_date = end_date
        self.dates = pd.date_range(start_date, end_date)

    @property
    def start_date(self):
        """Return the start date."""
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Set the start date."""
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise AttributeError("Invalid. Could not set the start date because the provided start date({}) is not "
                                 "a string in valid format (2018-01-01).".format(start_date))
        a_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        try:
            if a_start_date < self.end_date:
                self._start_date = a_start_date
            else:
                raise ValueError("Invalid. Could not set the start date because the provided start date ({}) "
                                 "is greater than the end date({}).".format(start_date, self.end_date))
        except AttributeError:
            self._start_date = a_start_date

    @property
    def end_date(self):
        """Return the end date."""
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Set the end date."""
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise AttributeError("Invalid. Could not set the end date because the provided end date({}) is not "
                                 "a string in valid format (2018-01-01).".format(end_date))
        a_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        try:
            if a_end_date > self._start_date:
                self._end_date = a_end_date
            else:
                raise ValueError("Invalid. Could not set the end date because the provided end date ({}) "
                                 "should be greater than the start date({}).".format(end_date, self._start_date))
        except AttributeError:
            self._end_date = a_end_date
