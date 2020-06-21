"""Contains the configurations or user input values needed to generate the shopper table."""
import datetime
from calendar import day_name


class Subject:
    """Represents the subject of observer pattern."""
    def __init__(self):
        """Initializes the subject with a list of observers."""
        self.__observers = []

    def register_observer(self, observer):
        """
        Registers the observer if it's not in the list of observers.
        :param observer: observer object to be added.
        """
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer):
        """
        Removes the observer if it's in the list of observers.
        :param observer: observer object to be removed.
        """
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self):
        """Notifies all observers of an update."""
        for observer in self.__observers:
            observer.update(self)


class DayOfWeekConfiguration(Subject):
    """Represents configuration for DayOfWeek class"""

    def __init__(self, mon_avg_traffic=800, tues_avg_traffic=1000, wed_avg_traffic=1200,
                 thurs_avg_traffic=900, fri_avg_traffic=2500,
                 sat_avg_traffic=4000, sun_avg_traffic=5000):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.mon_avg_traffic = mon_avg_traffic
        self.tues_avg_traffic = tues_avg_traffic
        self.wed_avg_traffic = wed_avg_traffic
        self.thurs_avg_traffic = thurs_avg_traffic
        self.fri_avg_traffic = fri_avg_traffic
        self.sat_avg_traffic = sat_avg_traffic
        self.sun_avg_traffic = sun_avg_traffic

    def get_shopper_traffic_by_day(self):
        """
        Returns a list of the average shopper traffic for
        each day of the week (Monday-Sunday).
        :return: a list of the average shopper traffic for each day of the week.
        """
        return [self._mon_avg_traffic, self._tues_avg_traffic, self._wed_avg_traffic,
                self._thurs_avg_traffic, self._fri_avg_traffic, self._sat_avg_traffic,
                self._sun_avg_traffic]

    @property
    def mon_avg_traffic(self):
        """Return the average traffic for Monday."""
        return self._mon_avg_traffic

    @mon_avg_traffic.setter
    def mon_avg_traffic(self, mon_avg_traffic):
        """Set the average traffic for Monday."""
        try:
            mon_avg_traffic = int(mon_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Monday because the provided"
            raise AttributeError(msg + " value ({}) is not an integer.".format(mon_avg_traffic))
        if mon_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Monday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(mon_avg_traffic))
        self._mon_avg_traffic = mon_avg_traffic
        self.notify_observers()

    @property
    def tues_avg_traffic(self):
        """Return the average traffic for Tuesday."""
        return self._tues_avg_traffic

    @tues_avg_traffic.setter
    def tues_avg_traffic(self, tues_avg_traffic):
        """Set the average traffic for Tuesday."""
        try:
            tues_avg_traffic = int(tues_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Tuesday because the provided"
            raise AttributeError(msg + " value ({}) is not an integer.".format(tues_avg_traffic))
        if tues_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Tuesday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(tues_avg_traffic))
        self._tues_avg_traffic = tues_avg_traffic
        self.notify_observers()

    @property
    def wed_avg_traffic(self):
        """Return the average traffic for Wednesday."""
        return self._wed_avg_traffic

    @wed_avg_traffic.setter
    def wed_avg_traffic(self, wed_avg_traffic):
        """Set the average traffic for Wednesday."""
        try:
            wed_avg_traffic = int(wed_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Wednesday because the provided"
            raise AttributeError(msg + " value ({}) is not an integer.".format(wed_avg_traffic))
        if wed_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Wednesday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(wed_avg_traffic))
        self._wed_avg_traffic = wed_avg_traffic
        self.notify_observers()

    @property
    def thurs_avg_traffic(self):
        """Return the average traffic for Thursday."""
        return self._thurs_avg_traffic

    @thurs_avg_traffic.setter
    def thurs_avg_traffic(self, thurs_avg_traffic):
        """Set the average traffic for Thursday."""
        try:
            thurs_avg_traffic = int(thurs_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Thursday because the provided"
            raise AttributeError(msg + " value ({}) is not an integer.".format(thurs_avg_traffic))
        if thurs_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Thursday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(thurs_avg_traffic))
        self._thurs_avg_traffic = thurs_avg_traffic
        self.notify_observers()

    @property
    def fri_avg_traffic(self):
        """Return the average traffic for Friday."""
        return self._fri_avg_traffic

    @fri_avg_traffic.setter
    def fri_avg_traffic(self, fri_avg_traffic):
        """Set the average traffic for Friday."""
        try:
            fri_avg_traffic = int(fri_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Friday because the provided "
            raise AttributeError(msg + "value ({}) is not an integer.".format(fri_avg_traffic))
        if fri_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Friday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(fri_avg_traffic))
        self._fri_avg_traffic = fri_avg_traffic
        self.notify_observers()

    @property
    def sat_avg_traffic(self):
        """Return the average traffic for Saturday."""
        return self._sat_avg_traffic

    @sat_avg_traffic.setter
    def sat_avg_traffic(self, sat_avg_traffic):
        """Set the average traffic for Saturday."""
        try:
            sat_avg_traffic = int(sat_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Saturday because the provided"
            raise AttributeError(msg + " value ({}) is not an integer.".format(sat_avg_traffic))
        if sat_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Saturday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(sat_avg_traffic))
        self._sat_avg_traffic = sat_avg_traffic
        self.notify_observers()

    @property
    def sun_avg_traffic(self):
        """Return the average traffic for Sunday."""
        return self._sun_avg_traffic

    @sun_avg_traffic.setter
    def sun_avg_traffic(self, sun_avg_traffic):
        """Set the average traffic for Sunday."""
        try:
            sun_avg_traffic = int(sun_avg_traffic)
        except ValueError:
            msg = "Invalid. Could not set the average traffic for Sunday because the provided"
            raise AttributeError(msg + " value ({}) is not an integer.".format(sun_avg_traffic))
        if sun_avg_traffic < 0:
            msg = "Invalid. Could not set the average traffic for Sunday because the value"
            raise AttributeError(msg + " ({}) is less than 0.".format(sun_avg_traffic))
        self._sun_avg_traffic = sun_avg_traffic
        self.notify_observers()


class HolidayConfiguration(Subject):
    """Represents configuration for Holiday class"""

    def __init__(self, holiday_percent=0.2, holiday_day_percent=1.4, holiday_week_percent=1.15):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.holiday_percent = holiday_percent
        self.holiday_day_percent = holiday_day_percent
        self.holiday_week_percent = holiday_week_percent

    def get_holiday_percentages(self):
        """
        Returns a list of average shopper traffic percentage increase/decrease
        for holiday, the day before a holiday, and the week leading up to a holiday.
        :return: a list of holiday related average shopper traffic percentage increase/decrease.
        """
        return [self._holiday_percent, self._holiday_day_percent, self._holiday_week_percent]

    @property
    def holiday_percent(self):
        """Return the percentage of normal traffic on a holiday."""
        return self._holiday_percent

    @holiday_percent.setter
    def holiday_percent(self, holiday_percent):
        """Set the percentage of normal traffic on a holiday."""
        try:
            holiday_percent = float(holiday_percent)
        except ValueError:
            msg = "Invalid. Could not set the percentage of normal traffic for a holiday "
            msg += "because the provided value ({}) is not a float.".format(holiday_percent)
            raise AttributeError(msg)
        if holiday_percent < 0.0 or holiday_percent > 1.0:
            msg = "Invalid. Could not set the the percentage of normal traffic for a holiday "
            msg += "because the value (" + str(holiday_percent)
            msg += ") is less than 0 or greater than 1."
            raise AttributeError(msg)
        self._holiday_percent = holiday_percent
        self.notify_observers()

    @property
    def holiday_day_percent(self):
        """Return the percentage of normal traffic for the day before a holiday."""
        return self._holiday_day_percent

    @holiday_day_percent.setter
    def holiday_day_percent(self, holiday_day_percent):
        """Set the percentage of normal traffic for the day before a holiday."""
        try:
            holiday_day_percent = float(holiday_day_percent)
        except ValueError:
            msg = "Invalid. Could not set the percentage of normal traffic for the day before "
            msg += "a holiday because the provided value "
            msg += "({}) is not a float.".format(holiday_day_percent)
            raise AttributeError(msg)
        if holiday_day_percent < 0.0:
            msg = "Invalid. Could not set the the percentage of normal traffic for the day "
            msg += "before a holiday because the "
            msg += "value ({}) is less than 0.".format(holiday_day_percent)
            raise AttributeError(msg)
        self._holiday_day_percent = holiday_day_percent
        self.notify_observers()

    @property
    def holiday_week_percent(self):
        """Return the percentage of normal traffic for the week before a holiday."""
        return self._holiday_week_percent

    @holiday_week_percent.setter
    def holiday_week_percent(self, holiday_week_percent):
        """Set the percentage of normal traffic for the week before a holiday."""
        try:
            holiday_week_percent = float(holiday_week_percent)
        except ValueError:
            msg = "Invalid. Could not set the percentage of normal traffic for the week before "
            msg += "a holiday because the provided value "
            msg += "({}) is not a float.".format(holiday_week_percent)
            raise AttributeError(msg)
        if holiday_week_percent < 0.0:
            msg = "Invalid. Could not set the the percentage of normal traffic for the week "
            msg += "before a holiday because the "
            msg += "value ({}) is less than 0.".format(holiday_week_percent)
            raise AttributeError(msg)
        self._holiday_week_percent = holiday_week_percent
        self.notify_observers()


class WeekdayConfiguration(Subject):
    """Represents configuration for Weekday class"""

    def __init__(self, min_time_spent=6, avg_time_spent=25, max_time_spent=75,
                 sunny_percentage=0.4, senior_percentage=0.3, open_time="6:00", close_time="21:00"):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.open_time = open_time
        self.close_time = close_time
        self.min_time_spent = min_time_spent
        self.avg_time_spent = avg_time_spent
        self.max_time_spent = max_time_spent
        self.sunny_percentage = sunny_percentage
        self.senior_percentage = senior_percentage

    @property
    def open_time(self):
        """Return the open time."""
        return self._open_time

    @open_time.setter
    def open_time(self, open_time):
        """Set the open time."""
        try:
            open_time = datetime.datetime.strptime(open_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the open time because the provided open time"
            msg += " ({}) is not a string in valid format (21:00).".format(open_time)
            raise AttributeError(msg)

        try:
            if open_time < self._close_time:
                self._open_time = open_time
            else:
                msg = "Invalid. Could not set the open time because the provided open time"
                msg += " ({}) is greater than the ".format(open_time)
                msg += "close time({}).".format(self._close_time)
                raise ValueError(msg)
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
            a_close_time = datetime.datetime.strptime(close_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the close time because the provided close time"
            msg += " ({}) is not a string in valid format (21:00).".format(close_time)
            raise AttributeError(msg)
        try:
            if a_close_time > self._open_time:
                self._close_time = a_close_time
            else:
                msg = "Invalid. Could not set the close time because the provided close time"
                msg += " ({}) is less than the open time({}).".format(close_time, self._open_time)
                raise ValueError(msg)
        except AttributeError:
            self._close_time = a_close_time

    def get_time_spent(self):
        """
        Returns a list of min, avg, max time spent by a shopper on average.
        :return: a list of min, avg, max time spent by a shopper on average.
        """
        return [self._min_time_spent, self._avg_time_spent, self._max_time_spent]

    @property
    def min_time_spent(self):
        """Return the minimum time a shopper spent in the store (in minutes)."""
        return self._min_time_spent

    @min_time_spent.setter
    def min_time_spent(self, min_time_spent):
        """Set the minimum time a shopper spent in the store (in minutes)."""
        try:
            min_time_spent = int(min_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the minimum time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(min_time_spent))
        if min_time_spent < 0:
            msg = "Invalid. Could not set the minimum time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(min_time_spent))
        self._min_time_spent = min_time_spent
        self.notify_observers()

    @property
    def avg_time_spent(self):
        """Return the average time a shopper spent in the store (in minutes)."""
        return self._avg_time_spent

    @avg_time_spent.setter
    def avg_time_spent(self, avg_time_spent):
        """Set the average time a shopper spent in the store (in minutes)."""
        try:
            avg_time_spent = int(avg_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the average time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(avg_time_spent))
        if avg_time_spent < 0:
            msg = "Invalid. Could not set the average time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(avg_time_spent))
        self._avg_time_spent = avg_time_spent
        self.notify_observers()

    @property
    def max_time_spent(self):
        """Return the maximum time a shopper spent in the store (in minutes)."""
        return self._max_time_spent

    @max_time_spent.setter
    def max_time_spent(self, max_time_spent):
        """Set the maximum time a shopper spent in the store (in minutes)."""
        try:
            max_time_spent = int(max_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the maximum time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(max_time_spent))
        if max_time_spent < 0:
            msg = "Invalid. Could not set the maximum time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(max_time_spent))
        self._max_time_spent = max_time_spent
        self.notify_observers()

    @property
    def sunny_percentage(self):
        """Return the chance that a given day is sunny as a percentage."""
        return self._sunny_percentage

    @sunny_percentage.setter
    def sunny_percentage(self, sunny_percentage):
        """Set the chance of sunny day."""
        try:
            sunny_percentage = float(sunny_percentage)
        except ValueError:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += " because the provided value ({}) is not a float.".format(sunny_percentage)
            raise AttributeError(msg)
        if sunny_percentage < 0.0:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += "because the value ({}) is less than 0.".format(sunny_percentage)
            raise AttributeError(msg)
        self._sunny_percentage = sunny_percentage
        self.notify_observers()

    @property
    def senior_percentage(self):
        """Return the percentage of seniors on a typical day."""
        return self._senior_percentage

    @senior_percentage.setter
    def senior_percentage(self, senior_percentage):
        """Set the percentage of senior shoppers."""
        try:
            senior_percentage = float(senior_percentage)
        except ValueError:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += " because the provided value ({}) is not a float.".format(senior_percentage)
            raise AttributeError(msg)
        if senior_percentage < 0.0:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += "because the value ({}) is less than 0.".format(senior_percentage)
            raise AttributeError(msg)
        self._senior_percentage = senior_percentage
        self.notify_observers()


class WeekendConfiguration(Subject):
    """Represents configuration for Weekend class"""

    def __init__(self, avg_time_spent=60, sunny_avg_time_spent=10, sunny_percent_traffic=1.4,
                 sunny_percentage=0.4, senior_percentage=0.3,
                 open_time="6:00", close_time="21:00"):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.open_time = open_time
        self.close_time = close_time
        self.avg_time_spent = avg_time_spent
        self.sunny_avg_time_spent = sunny_avg_time_spent
        self.sunny_percent_traffic = sunny_percent_traffic
        self.sunny_percentage = sunny_percentage
        self.senior_percentage = senior_percentage

    @property
    def open_time(self):
        """Return the open time."""
        return self._open_time

    @open_time.setter
    def open_time(self, open_time):
        """Set the open time."""
        try:
            open_time = datetime.datetime.strptime(open_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the open time because the provided open time"
            msg += " ({}) is not a string in valid format (21:00).".format(open_time)
            raise AttributeError(msg)

        try:
            if open_time < self._close_time:
                self._open_time = open_time
            else:
                msg = "Invalid. Could not set the open time because the provided open time"
                msg += " ({}) is greater than ".format(open_time)
                msg += "the close time({}).".format(self._close_time)
                raise ValueError(msg)
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
            a_close_time = datetime.datetime.strptime(close_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the close time because the provided close time"
            msg += " ({}) is not a string in valid format (21:00).".format(close_time)
            raise AttributeError(msg)
        try:
            if a_close_time > self._open_time:
                self._close_time = a_close_time
            else:
                msg = "Invalid. Could not set the close time because the provided close time"
                msg += " ({}) is less than the open time({}).".format(close_time, self._open_time)
                raise ValueError(msg)
        except AttributeError:
            self._close_time = a_close_time

    @property
    def avg_time_spent(self):
        """Return the average time a shopper spent in the store (in minutes)."""
        return self._avg_time_spent

    @avg_time_spent.setter
    def avg_time_spent(self, avg_time_spent):
        """Set the average time a shopper spent in the store (in minutes)."""
        try:
            avg_time_spent = int(avg_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the average time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(avg_time_spent))
        if avg_time_spent < 0:
            msg = "Invalid. Could not set the average time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(avg_time_spent))
        self._avg_time_spent = avg_time_spent
        self.notify_observers()

    @property
    def sunny_avg_time_spent(self):
        """Return the average time a shopper spent in the store on a sunny day (in minutes)."""
        return self._sunny_avg_time_spent

    @sunny_avg_time_spent.setter
    def sunny_avg_time_spent(self, sunny_avg_time_spent):
        """Set the average time a shopper spent in the store on a sunny day (in minutes)."""
        try:
            sunny_avg_time_spent = int(sunny_avg_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the average time spent on a sunny day because the "
            msg += "provided value ({}) is not an integer.".format(sunny_avg_time_spent)
            raise AttributeError(msg)
        if sunny_avg_time_spent < 0:
            msg = "Invalid. Could not set the average time spent on a sunny day because the "
            msg += "value ({}) is less than 0.".format(sunny_avg_time_spent)
            raise AttributeError(msg)
        self._sunny_avg_time_spent = sunny_avg_time_spent
        self.notify_observers()

    @property
    def sunny_percent_traffic(self):
        """Return the percentage of traffic increase on a sunny day."""
        return self._sunny_percent_traffic

    @sunny_percent_traffic.setter
    def sunny_percent_traffic(self, sunny_percent_traffic):
        """Set the percentage of traffic increase on a sunny day."""
        try:
            sunny_percent_traffic = float(sunny_percent_traffic)
        except ValueError:
            msg = "Invalid. Could not set the percentage of traffic increase on a sunny day "
            msg += " because the provided value ({}) is not a float.".format(sunny_percent_traffic)
            raise AttributeError(msg)
        if sunny_percent_traffic < 0.0:
            msg = "Invalid. Could not set the percentage of traffic increase on a sunny day "
            msg += "because the value ({}) is less than 0.".format(sunny_percent_traffic)
            raise AttributeError(msg)
        self._sunny_percent_traffic = sunny_percent_traffic
        self.notify_observers()

    @property
    def sunny_percentage(self):
        """Return the chance that a given day is sunny as a percentage."""
        return self._sunny_percentage

    @sunny_percentage.setter
    def sunny_percentage(self, sunny_percentage):
        """Set the chance of sunny day."""
        try:
            sunny_percentage = float(sunny_percentage)
        except ValueError:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += " because the provided value ({}) is not a float.".format(sunny_percentage)
            raise AttributeError(msg)
        if sunny_percentage < 0.0:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += "because the value ({}) is less than 0.".format(sunny_percentage)
            raise AttributeError(msg)
        self._sunny_percentage = sunny_percentage
        self.notify_observers()

    @property
    def senior_percentage(self):
        """Return the percentage of seniors on a typical day."""
        return self._senior_percentage

    @senior_percentage.setter
    def senior_percentage(self, senior_percentage):
        """Set the percentage of senior shoppers."""
        try:
            senior_percentage = float(senior_percentage)
        except ValueError:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += " because the provided value ({}) is not a float.".format(senior_percentage)
            raise AttributeError(msg)
        if senior_percentage < 0.0:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += "because the value ({}) is less than 0.".format(senior_percentage)
            raise AttributeError(msg)
        self._senior_percentage = senior_percentage
        self.notify_observers()

class LunchRushConfiguration(Subject):
    """Represents configuration for LunchRush class"""

    def __init__(self, avg_time_spent=10, sunny_percentage=0.4, senior_percentage=0.3,
                 start_time="12:00", end_time="13:00"):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.start_time = start_time
        self.end_time = end_time
        self.avg_time_spent = avg_time_spent
        self.sunny_percentage = sunny_percentage
        self.senior_percentage = senior_percentage

    @property
    def start_time(self):
        """Return the start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Set the start time."""
        try:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the open time because the provided start time"
            msg += " ({}) is not a string in valid format (12:00).".format(start_time)
            raise AttributeError(msg)

        try:
            if start_time < self._end_time:
                self._start_time = start_time
            else:
                msg = "Invalid. Could not set the open time because the provided start time"
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
            a_end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the end time because the provided end time"
            msg += " ({}) is not a string in valid format (13:00).".format(end_time)
            raise AttributeError(msg)
        try:
            if a_end_time > self._start_time:
                self._end_time = a_end_time
            else:
                msg = "Invalid. Could not set the end time because the provided end time"
                msg += " ({}) is less than the start time({}).".format(end_time, self._start_time)
                raise ValueError(msg)
        except AttributeError:
            self._end_time = a_end_time

    @property
    def avg_time_spent(self):
        """Return the average time a shopper spent in the store (in minutes)."""
        return self._avg_time_spent

    @avg_time_spent.setter
    def avg_time_spent(self, avg_time_spent):
        """Set the average time a shopper spent in the store (in minutes)."""
        try:
            avg_time_spent = int(avg_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the average time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(avg_time_spent))
        if avg_time_spent < 0:
            msg = "Invalid. Could not set the average time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(avg_time_spent))
        self._avg_time_spent = avg_time_spent
        self.notify_observers()

    @property
    def sunny_percentage(self):
        """Return the chance that a given day is sunny as a percentage."""
        return self._sunny_percentage

    @sunny_percentage.setter
    def sunny_percentage(self, sunny_percentage):
        """Set the chance of sunny day."""
        try:
            sunny_percentage = float(sunny_percentage)
        except ValueError:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += " because the provided value ({}) is not a float.".format(sunny_percentage)
            raise AttributeError(msg)
        if sunny_percentage < 0.0:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += "because the value ({}) is less than 0.".format(sunny_percentage)
            raise AttributeError(msg)
        self._sunny_percentage = sunny_percentage
        self.notify_observers()

    @property
    def senior_percentage(self):
        """Return the percentage of seniors on a typical day."""
        return self._senior_percentage

    @senior_percentage.setter
    def senior_percentage(self, senior_percentage):
        """Set the percentage of senior shoppers."""
        try:
            senior_percentage = float(senior_percentage)
        except ValueError:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += " because the provided value ({}) is not a float.".format(senior_percentage)
            raise AttributeError(msg)
        if senior_percentage < 0.0:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += "because the value ({}) is less than 0.".format(senior_percentage)
            raise AttributeError(msg)
        self._senior_percentage = senior_percentage
        self.notify_observers()

class DinnerRushConfiguration(Subject):
    """Represents configuration for DinnerRush class"""

    def __init__(self, avg_time_spent=10, sunny_percentage=0.4, senior_percentage=0.3,
                 start_time="17:00", end_time="18:30"):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.start_time = start_time
        self.end_time = end_time
        self.avg_time_spent = avg_time_spent
        self.sunny_percentage = sunny_percentage
        self.senior_percentage = senior_percentage

    @property
    def start_time(self):
        """Return the start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Set the start time."""
        try:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the open time because the provided start time"
            msg += " ({}) is not a string in valid format (12:00).".format(start_time)
            raise AttributeError(msg)

        try:
            if start_time < self._end_time:
                self._start_time = start_time
            else:
                msg = "Invalid. Could not set the open time because the provided start time"
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
            a_end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the end time because the provided end time"
            msg += " ({}) is not a string in valid format (13:00).".format(end_time)
            raise AttributeError(msg)
        try:
            if a_end_time > self._start_time:
                self._end_time = a_end_time
            else:
                msg = "Invalid. Could not set the end time because the provided end time"
                msg += " ({}) is less than the start time({}).".format(end_time, self._start_time)
                raise ValueError(msg)
        except AttributeError:
            self._end_time = a_end_time

    @property
    def avg_time_spent(self):
        """Return the average time a shopper spent in the store (in minutes)."""
        return self._avg_time_spent

    @avg_time_spent.setter
    def avg_time_spent(self, avg_time_spent):
        """Set the average time a shopper spent in the store (in minutes)."""
        try:
            avg_time_spent = int(avg_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the average time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(avg_time_spent))
        if avg_time_spent < 0:
            msg = "Invalid. Could not set the average time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(avg_time_spent))
        self._avg_time_spent = avg_time_spent
        self.notify_observers()

    @property
    def sunny_percentage(self):
        """Return the chance that a given day is sunny as a percentage."""
        return self._sunny_percentage

    @sunny_percentage.setter
    def sunny_percentage(self, sunny_percentage):
        """Set the chance of sunny day."""
        try:
            sunny_percentage = float(sunny_percentage)
        except ValueError:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += " because the provided value ({}) is not a float.".format(sunny_percentage)
            raise AttributeError(msg)
        if sunny_percentage < 0.0:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += "because the value ({}) is less than 0.".format(sunny_percentage)
            raise AttributeError(msg)
        self._sunny_percentage = sunny_percentage
        self.notify_observers()

    @property
    def senior_percentage(self):
        """Return the percentage of seniors on a typical day."""
        return self._senior_percentage

    @senior_percentage.setter
    def senior_percentage(self, senior_percentage):
        """Set the percentage of senior shoppers."""
        try:
            senior_percentage = float(senior_percentage)
        except ValueError:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += " because the provided value ({}) is not a float.".format(senior_percentage)
            raise AttributeError(msg)
        if senior_percentage < 0.0:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += "because the value ({}) is less than 0.".format(senior_percentage)
            raise AttributeError(msg)
        self._senior_percentage = senior_percentage
        self.notify_observers()

class SeniorRushConfiguration(Subject):
    """Represents configuration for SeniorRush class"""

    def __init__(self, min_time_spent=45, max_time_spent=60,
                 sunny_percentage=0.4, senior_percentage=0.6,
                 start_time="10:00", end_time="12:00", day_of_week="Tuesday"):
        """Initializes the configuration."""
        Subject.__init__(self)
        self.start_time = start_time
        self.end_time = end_time
        self.min_time_spent = min_time_spent
        self.max_time_spent = max_time_spent
        self.day_of_week = day_of_week
        self.sunny_percentage = sunny_percentage
        self.senior_percentage = senior_percentage

    @property
    def day_of_week(self):
        """Return the day of week as a string."""
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, day_of_week):
        if not isinstance(day_of_week, str):
            raise TypeError("Invalid. Could not set the day of week because the provided"
                            " {} is not a string.".format(day_of_week))
        if day_of_week not in day_name:
            raise AttributeError("Invalid. Could not set the day of week because the provided"
                                 " {} is an invalid day of week.".format(day_of_week))
        self._day_of_week = day_of_week

    @property
    def start_time(self):
        """Return the start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Set the start time."""
        try:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the open time because the provided start time"
            msg += " ({}) is not a string in valid format (12:00).".format(start_time)
            raise AttributeError(msg)

        try:
            if start_time < self._end_time:
                self._start_time = start_time
            else:
                msg = "Invalid. Could not set the open time because the provided start time"
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
            a_end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
        except (TypeError, ValueError):
            msg = "Invalid. Could not set the end time because the provided end time"
            msg += " ({}) is not a string in valid format (13:00).".format(end_time)
            raise AttributeError(msg)
        try:
            if a_end_time > self._start_time:
                self._end_time = a_end_time
            else:
                msg = "Invalid. Could not set the end time because the provided end time"
                msg += " ({}) is less than the start time({}).".format(end_time, self._start_time)
                raise ValueError(msg)
        except AttributeError:
            self._end_time = a_end_time

    @property
    def min_time_spent(self):
        """Return the minimum time a shopper spent in the store (in minutes)."""
        return self._min_time_spent

    @min_time_spent.setter
    def min_time_spent(self, min_time_spent):
        """Set the minimum time a shopper spent in the store (in minutes)."""
        try:
            min_time_spent = int(min_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the minimum time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(min_time_spent))
        if min_time_spent < 0:
            msg = "Invalid. Could not set the minimum time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(min_time_spent))
        self._min_time_spent = min_time_spent
        self.notify_observers()

    @property
    def max_time_spent(self):
        """Return the maximum time a shopper spent in the store (in minutes)."""
        return self._max_time_spent

    @max_time_spent.setter
    def max_time_spent(self, max_time_spent):
        """Set the maximum time a shopper spent in the store (in minutes)."""
        try:
            max_time_spent = int(max_time_spent)
        except ValueError:
            msg = "Invalid. Could not set the maximum time spent because the provided value "
            raise AttributeError(msg + "({}) is not an integer.".format(max_time_spent))
        if max_time_spent < 0:
            msg = "Invalid. Could not set the maximum time spent because the value "
            raise AttributeError(msg + "({}) is less than 0.".format(max_time_spent))
        self._max_time_spent = max_time_spent
        self.notify_observers()

    @property
    def sunny_percentage(self):
        """Return the chance that a given day is sunny as a percentage."""
        return self._sunny_percentage

    @sunny_percentage.setter
    def sunny_percentage(self, sunny_percentage):
        """Set the chance of sunny day."""
        try:
            sunny_percentage = float(sunny_percentage)
        except ValueError:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += " because the provided value ({}) is not a float.".format(sunny_percentage)
            raise AttributeError(msg)
        if sunny_percentage < 0.0:
            msg = "Invalid. Could not set the chance of sunny day as a percentage "
            msg += "because the value ({}) is less than 0.".format(sunny_percentage)
            raise AttributeError(msg)
        self._sunny_percentage = sunny_percentage
        self.notify_observers()

    @property
    def senior_percentage(self):
        """Return the percentage of seniors on a typical day."""
        return self._senior_percentage

    @senior_percentage.setter
    def senior_percentage(self, senior_percentage):
        """Set the percentage of senior shoppers."""
        try:
            senior_percentage = float(senior_percentage)
        except ValueError:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += " because the provided value ({}) is not a float.".format(senior_percentage)
            raise AttributeError(msg)
        if senior_percentage < 0.0:
            msg = "Invalid. Could not set the percentage of senior shoppers "
            msg += "because the value ({}) is less than 0.".format(senior_percentage)
            raise AttributeError(msg)
        self._senior_percentage = senior_percentage
        self.notify_observers()
