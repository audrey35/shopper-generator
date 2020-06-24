"""
Holds the percentage increase or decrease of shoppers during a holiday.
Used to change number of shoppers during a holiday.
"""
import holidays
import pandas as pd


class HolidayModifiers:
    """
    Holds the percentage increase or decrease of shoppers during a holiday.
    Used to change number of shoppers during a holiday.
    """

    holidays = holidays.US()

    def __init__(self, holiday_percent=0.2, day_before_percent=0.4, week_before_percent=0.15):
        """
        Initializes HolidayModifiers.
        :param holiday_percent: percent decrease in average shopper traffic on a holiday (0.2).
        :param day_before_percent: percent increase in average shopper traffic the day before a
        holiday as a decimal (0.4).
        :param week_before_percent: percent increase in average shopper traffic during the week
        leading up to a holiday as a decimal (0.15).
        """
        self.holiday_percent = holiday_percent
        self.day_before_percent = day_before_percent
        self.week_before_percent = week_before_percent

    def apply_holiday_modifier(self, date, num_of_shoppers):
        """
        Returns the number of shoppers after applying holiday percent
        changes if applicable.
        :param date: date as a datetime object.
        :param num_of_shoppers: current number of shoppers for the given date.
        :return: updated number of shoppers for the given date.
        """
        if self.__is_holiday(date):
            return round(num_of_shoppers * self.holiday_percent)
        if self.__is_day_before_holiday(date):
            return round(num_of_shoppers * (1 + self.day_before_percent))
        if self.__is_week_before_holiday(date):
            return round(num_of_shoppers * (1 + self.week_before_percent))
        return num_of_shoppers

    def __is_holiday(self, date):
        """
        Returns true if the given date is a holiday. False otherwise.
        :param date: date as a datetime object.
        :return: true if the given date is a holiday. False otherwise.
        """
        return date in self.holidays

    def __is_day_before_holiday(self, date):
        """
        Returns true if the given date is one day before a holiday. False otherwise.
        :param date: the date as a datetime object.
        :return: true if the given date is one day before a holiday. False otherwise.
        """
        date_ahead = date + pd.Timedelta('1 days')
        return date_ahead in self.holidays

    def __is_week_before_holiday(self, date):
        """
        Returns true if the given date is 2 to 7 days before a holiday. False otherwise.
        :param date: the date as a datetime object.
        :return: true if the given date is 2 to 7 days before a holiday. False otherwise.
        """
        time_deltas = pd.timedelta_range(start='2 days', periods=5)
        for delta in time_deltas:
            test_date = date + delta
            if test_date in self.holidays:
                return True
        return False
