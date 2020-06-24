import calendar
from datetime import datetime

from shoppermodel.day import Day


class StoreModel:

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
        if self.days_of_week[day_of_week.day_name] is None:
            self.days_of_week[day_of_week.day_name] = day_of_week
        else:
            raise ValueError('The day of week ' + day_of_week.day_name + ' is already defined')

    def create_day(self, date):
        day_name = calendar.day_name[date.weekday()]
        # get avg number of shoppers based on day of week
        num_of_shoppers = self.days_of_week[day_name].shopper_traffic
        # check if the date is a holiday
        num_of_shoppers = self.holiday_modifiers.apply_holiday_modifier(date, num_of_shoppers)

        # # sunny and weekend check
        # is_sunny = False
        # if date.weekday() in [5, 6]:
        #     # 30% chance that day is sunny
        #     if np.random.choice(a=np.array([True, False]),
        #                         p=[self.sunny_chance_percent, 1 - self.sunny_chance_percent]):
        #         num_of_shoppers = round(num_of_shoppers * (1 + self.sunny_traffic_percent))
        #         is_sunny = True

        # create a Day object and return it
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
