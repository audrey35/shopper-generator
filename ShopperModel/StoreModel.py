import time


#TODO put in package, rename to config

class StoreModel:

    def __init__(self, open_time, close_time, lunch_rush, dinner_rush, percent_senior):
        self.open_time = open_time
        self.close_time = close_time
        self.lunch_rush = lunch_rush
        self.dinner_rush = dinner_rush
        self.percent_senior = percent_senior
        self.days_of_week = {'Monday': None, 'Tuesday': None, 'Wednesday': None, 'Thursday': None, 'Friday': None,
                             'Saturday': None, 'Sunday': None}

    def add_day_of_week(self, day_of_week):
        if self.days_of_week[day_of_week.name] is not None:
            self.days_of_week[day_of_week.name] = day_of_week
        else:
            raise ValueError('The day of week ' + day_of_week.name + ' is already defined')

    @property
    def open_time(self):
        """Return the open time."""
        return self._open_time

    @open_time.setter
    def open_time(self, open_time):
        """Set the open time."""
        try:
            open_time = time.strptime(open_time, '%H:%M')
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the open time because the provided open time ({}) is"
                                 " not a string in valid format (21:00).".format(open_time))

        try:
            if open_time < self._close_time:
                self._open_time = open_time
            else:
                raise ValueError("Invalid. Could not set the open time because the provided open time ({}) is"
                                 " greater than the close time({}).".format(open_time, self._close_time))
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
            time.strptime(close_time, '%H:%M')
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the close time because the provided close time ({}) is"
                                 " not a string in valid format (21:00).".format(close_time))
        a_close_time = time.strptime(close_time, '%H:%M')
        try:
            if a_close_time > self._open_time:
                self._close_time = a_close_time
            else:
                raise ValueError("Invalid. Could not set the close time because the provided close time ({}) is"
                                 " less than the open time({}).".format(close_time, self._open_time))
        except AttributeError:
            self._close_time = a_close_time