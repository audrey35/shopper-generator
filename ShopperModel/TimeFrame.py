import holidays
import pandas as pd


class TimeFrame:
    """
    The TimeFrame represents the time period for the shopper behavior being tracked.
    It knows whether a date is a holiday and can create a list of dates within the time period.
    """
    holidays = holidays.US()

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.dates = pd.date_range(start_date, end_date)
        self.days = []

    def is_holiday(self, date):
        return date in self.holidays

    def is_day_before_holiday(self, date):
        date_ahead = date + pd.Timedelta('1 days')
        return date_ahead in self.holidays

    def is_within_week_of_holiday(self, date):
        time_deltas = pd.timedelta_range(start='2 days', periods=6)
        within = False
        for delta in time_deltas:
            date += delta
            if date in self.holidays:
                within = True
                break
        return within
