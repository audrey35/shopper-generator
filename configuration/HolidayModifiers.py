import holidays
import pandas as pd


class HolidayModifiers:
    """
    Holds the percentage increase or decrease of shoppers during a holiday. Used to change number of shoppers during
    a holiday.
    """

    holidays = holidays.US()

    def __init__(self, holiday_percent=0.2, day_before_percent=0.4, week_before_percent=0.15):
        self.holiday_percent = holiday_percent
        self.day_before_percent = day_before_percent
        self.week_before_percent = week_before_percent

    def apply_holiday_modifier(self, date, num_of_shoppers):

        if self.__is_holiday(date):
            return round(num_of_shoppers * self.holiday_percent)
        elif self.__is_day_before_holiday(date):
            return round(num_of_shoppers * (1 + self.day_before_percent))
        elif self.__is_week_before_holiday(date):
            return round(num_of_shoppers * (1 + self.week_before_percent))
        else:
            return num_of_shoppers

    def __is_holiday(self, date):
        return date in self.holidays

    def __is_day_before_holiday(self, date):
        date_ahead = date + pd.Timedelta('1 days')
        return date_ahead in self.holidays

    def __is_week_before_holiday(self, date):
        time_deltas = pd.timedelta_range(start='2 days', periods=6)
        for delta in time_deltas:
            test_date = date + delta
            if test_date in self.holidays:
                return True
        return False
