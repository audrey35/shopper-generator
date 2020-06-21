"""Contains classes used to generate a shopper table."""
import datetime
from calendar import day_name
import numpy
import holidays
from Shoppers import DayOfWeekConfiguration, WeekdayConfiguration, WeekendConfiguration
from Shoppers import LunchRushConfiguration, DinnerRushConfiguration, SeniorRushConfiguration
from Shoppers import HolidayConfiguration


def random_min_max(minimum, maximum, size):
    """
    Returns a numpy array of random values.
    :param minimum: minimum allowed value.
    :param maximum: maximum allowed value.
    :param size: size of the output array.
    :return: a numpy array of random values.
    """
    result = numpy.random.rand(size) * (maximum - minimum) + minimum
    return result


def random_avg_int(avg, size):
    """
    Returns a numpy array of random integers with a normal distribution.
    :param avg: average value set for the normal distribution.
    :param size: size of the output array.
    :return: a numpy array of random integers.
    """
    result = numpy.round(numpy.random.normal(loc=avg, size=size)).astype(int)
    return result


def random_min_max_int(minimum, maximum, size):
    """
        Returns a numpy array of random integers.
        :param minimum: minimum allowed integer.
        :param maximum: maximum allowed integer.
        :param size: size of the output array.
        :return: a numpy array of random integers.
        """
    result = numpy.round(numpy.random.rand(size) * (maximum - minimum) + minimum).astype(int)
    return result


def random_avg_min_max_int(minimum, avg, maximum, size):
    """
    Returns a numpy array of random integers.
    :param minimum: minimum allowed integer.
    :param avg: average value set for the normal distribution.
    :param maximum: maximum allowed integer.
    :param size: size of the output array.
    :return: a numpy array of random integers.
    """
    result1 = random_avg_int(avg, round(size * 0.98))
    result2 = random_min_max_int(minimum, maximum, round(size * 0.02))
    result = numpy.concatenate((result1, result2))
    return result


def random_choice(sample_list: list, probability_list=None, size=None):
    """
    Returns a numpy array of random sample from a given list.
    :param sample_list: a random sample is generated from its elements.
    :param probability_list: probabilities associated with each element in sample_list.
    :param size: size of the output array.
    :return: a numpy array of random sample from a given list.
    """
    result = numpy.random.choice(sample_list, p=probability_list, size=size)
    return result


class DayOfWeek:
    """Represents shopper traffic for one of the days in a week."""

    def __init__(self, day_of_week_configuration: DayOfWeekConfiguration):
        """
        Initializes the DayOfWeek class with a configuration.
        :param day_of_week_configuration: DayOfWeekConfiguration object.
        """
        if isinstance(day_of_week_configuration, DayOfWeekConfiguration):
            self.__configuration = day_of_week_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a DayOfWeekConfiguration object.")

    def get_average_shopper_traffic(self, date: datetime.datetime):
        """
        Returns the average shopper traffic for the given date.
        :param date: date as a datetime object.
        :return: the average shopper traffic for the given date as an integer.
        """
        shopper_count_by_day = self.__configuration.get_shopper_traffic_by_day()
        avg_traffic = shopper_count_by_day[date.weekday()]
        shopper_traffic = int(random_avg_int(avg=avg_traffic, size=100)[0])
        return shopper_traffic

    def get_day_of_week(self, date: datetime.datetime):
        """
        Returns the day of week for a given date as a string.
        :param date: date as a datetime object.
        :return: day of week for a given date as a string.
        """
        return day_name[date.weekday()]

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated DayOfWeekConfiguration object.
        """
        self.__configuration = configuration


class Holiday:
    """Represents shopper traffic for a holiday related date."""

    def __init__(self, holiday_configuration: HolidayConfiguration):
        """
        Initializes the Holiday object with a given configuration.
        :param holiday_configuration: HolidayConfiguration object.
        """
        if isinstance(holiday_configuration, HolidayConfiguration):
            self.__configuration = holiday_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a HolidayConfiguration object.")

    def get_average_shopper_traffic(self, date: datetime.datetime, shopper_traffic: int):
        """
        Returns the updated average shopper traffic for the date as an integer
        and the number of days before a holiday as an integer.
        :param date: date as a datetime object.
        :param shopper_traffic: current shopper traffic as an integer.
        :return: a tuple of the updated average shopper traffic for the date as an integer
        and the number of days before a holiday as an integer.
        """
        if not isinstance(date, datetime.datetime):
            raise TypeError("Invalid. Date should be a datetime object.")
        if not isinstance(shopper_traffic, int):
            raise TypeError("Invalid. Shopper traffic should be an integer.")
        shopper_counts = self.__configuration.get_holiday_percentages()
        holiday_list = holidays.US()

        # date is a holiday
        if date in holiday_list:
            return round(shopper_counts[0] * shopper_traffic), 0

        # date is one day before a holiday
        date_ahead = date + datetime.timedelta(days=1)
        if date_ahead in holiday_list:
            return round(shopper_counts[1] * shopper_traffic), 1

        # date is 2 to 7 days before a holiday
        for delta in list(range(2, 8)):
            new_date = date + datetime.timedelta(days=delta)
            if new_date in holiday_list:
                return round(shopper_counts[2] * shopper_traffic), delta

        return shopper_traffic, -1

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated HolidayConfiguration object.
        """
        self.__configuration = configuration


class Weekday:
    """Represents shopper table for a single day."""

    def __init__(self, weekday_configuration: WeekdayConfiguration):
        """
        Initializes the Holiday object with a given configuration.
        :param weekday_configuration: WeekdayConfiguration object.
        """
        if isinstance(weekday_configuration, WeekdayConfiguration):
            self.__configuration = weekday_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a WeekdayConfiguration object.")

    def get_day_dictionary(self, date: datetime.datetime, shopper_traffic: int,
                           day_of_week: str, num_day_holiday: int):
        """
        Returns the shopper table for a single day and number of shoppers per hour.
        :param date: date as a datetime object.
        :param shopper_traffic: current shopper traffic as an integer.
        :param day_of_week: day of week as a string (i.e., Monday).
        :param num_day_holiday: number of days before a holiday (-1 means not applicable).
        :return: a tuple of the shopper table for a single day as a dictionary and
        number of shoppers per hour.
        """
        if not isinstance(date, datetime.datetime):
            raise TypeError("Invalid. Date should be a datetime object.")
        if not isinstance(shopper_traffic, int):
            raise TypeError("Invalid. Shopper traffic should be an integer.")
        if not isinstance(day_of_week, str):
            raise TypeError("Invalid. Day of week should be a string.")
        if not isinstance(num_day_holiday, int):
            raise TypeError("Invalid. Number of days before a holiday should be an integer.")

        # number of shoppers per hour
        start = self.__configuration.open_time
        start = datetime.datetime.combine(date, start)
        end = self.__configuration.close_time
        end = datetime.datetime.combine(date, end)
        num_hours = end.hour - start.hour
        hour_traffic = round(shopper_traffic / (1.0 * num_hours))

        # date is a weekend
        if date.weekday() in [5, 6]:
            return {}, hour_traffic

        shopper_table = {"Date": [date] * shopper_traffic,
                         "Holiday": [num_day_holiday] * shopper_traffic,
                         "DayOfWeek": [day_of_week] * shopper_traffic,
                         "Sunny": [],
                         "TimeIn": [], "TimeSpent": [], "Senior": []}

        sunny = self.__configuration.sunny_percentage
        sunny = random_choice(sample_list=[True, False], probability_list=[sunny, 1 - sunny])
        shopper_table["Sunny"] = [bool(sunny)] * shopper_traffic

        time_in = random_min_max(minimum=start, maximum=end, size=shopper_traffic)
        shopper_table["TimeIn"] = time_in.tolist()

        mints = self.__configuration.min_time_spent
        avg = self.__configuration.avg_time_spent
        maxi = self.__configuration.max_time_spent
        time_spent = random_avg_min_max_int(minimum=mints, avg=avg, maximum=maxi,
                                            size=shopper_traffic)
        shopper_table["TimeSpent"] = time_spent.tolist()

        senior = self.__configuration.senior_percentage
        senior = random_choice(sample_list=[True, False], probability_list=[senior, 1 - senior],
                               size=shopper_traffic)
        shopper_table["Senior"] = senior.tolist()

        return shopper_table, hour_traffic

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated WeekdayConfiguration object.
        """
        self.__configuration = configuration


class Weekend:
    """Represents shopper table for a single weekend day."""

    def __init__(self, weekend_configuration: WeekendConfiguration):
        """
        Initializes the Holiday object with a given configuration.
        :param weekend_configuration: WeekendConfiguration object.
        """
        if isinstance(weekend_configuration, WeekendConfiguration):
            self.__configuration = weekend_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a WeekendConfiguration object.")

    def get_day_dictionary(self, date: datetime.datetime, shopper_traffic: int,
                           day_of_week: str, num_day_holiday: int):
        """
        Returns the shopper table for a single day and number of shoppers per hour.
        :param date: date as a datetime object.
        :param shopper_traffic: current shopper traffic as an integer.
        :param day_of_week: day of week as a string (i.e., Monday).
        :param num_day_holiday: number of days before a holiday (-1 means not applicable).
        :return: a tuple of the shopper table for a single day as a dictionary and
        number of shoppers per hour.
        """
        if not isinstance(date, datetime.datetime):
            raise TypeError("Invalid. Date should be a datetime object.")
        if not isinstance(shopper_traffic, int):
            raise TypeError("Invalid. Shopper traffic should be an integer.")
        if not isinstance(day_of_week, str):
            raise TypeError("Invalid. Day of week should be a string.")
        if not isinstance(num_day_holiday, int):
            raise TypeError("Invalid. Number of days before a holiday should be an integer.")

        # number of shoppers per hour
        start = self.__configuration.open_time
        start = datetime.datetime.combine(date, start)
        end = self.__configuration.close_time
        end = datetime.datetime.combine(date, end)
        num_hours = end.hour - start.hour
        hour_traffic = round(shopper_traffic / (1.0 * num_hours))

        # date is a weekday
        if date.weekday() not in [5, 6]:
            return {}, hour_traffic

        shopper_table = {"Date": [date] * shopper_traffic,
                         "Holiday": [num_day_holiday] * shopper_traffic,
                         "DayOfWeek": [day_of_week] * shopper_traffic,
                         "Sunny": [],
                         "TimeIn": [], "TimeSpent": [], "Senior": []}

        sunny = self.__configuration.sunny_percentage
        sunny = bool(random_choice(sample_list=[True, False], probability_list=[sunny, 1 - sunny]))
        traffic = round(self.__configuration.sunny_percent_traffic * shopper_traffic)

        shopper_table["Sunny"] = [sunny] * shopper_traffic

        time_in = random_min_max(minimum=start, maximum=end, size=shopper_traffic)

        avg = self.__configuration.avg_time_spent
        time_spent = random_avg_int(avg=avg, size=shopper_traffic).tolist()

        senior = self.__configuration.senior_percentage
        senior = random_choice(sample_list=[True, False], probability_list=[senior, 1 - senior],
                               size=shopper_traffic)

        if sunny:
            # TODO adjust for sunny percent being 1.4 not 0.4
            temp = shopper_traffic + traffic
            shopper_table["Date"] = [date] * temp
            shopper_table["DayOfWeek"] = [day_of_week] * temp
            shopper_table["Holiday"] = [num_day_holiday] * temp
            shopper_table["Sunny"] = [sunny] * temp
            time_in = random_min_max(minimum=start, maximum=end, size=temp)
            avg = self.__configuration.sunny_avg_time_spent
            time_spent += random_avg_int(avg=avg, size=traffic).tolist()
            senior = random_choice(sample_list=[True, False], probability_list=[senior, 1 - senior],
                                   size=temp)

        shopper_table["TimeIn"] = time_in.tolist()
        shopper_table["TimeSpent"] = time_spent
        shopper_table["Senior"] = senior.tolist()

        return shopper_table, hour_traffic

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated WeekendConfiguration object.
        """
        self.__configuration = configuration

class LunchRush:
    """Represents shopper table for a single day."""

    def __init__(self, lunch_configuration: LunchRushConfiguration):
        """
        Initializes the LunchRush object with a given configuration.
        :param lunch_configuration: LunchRushConfiguration object.
        """
        if isinstance(lunch_configuration, LunchRushConfiguration):
            self.__configuration = lunch_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a LunchRushConfiguration object.")

    def get_day_dictionary(self, shopper_table_dict: dict, hour_traffic: int):
        """
        Returns a shopper table for a single day.
        :param shopper_table_dict: shopper table for a single day as a dictionary.
        :param hour_traffic: shopper traffic per hour as an integer.
        :return: shopper table for a single day as a dictionary.
        """
        if not isinstance(shopper_table_dict, dict):
            raise TypeError("Invalid. Shopper table dict should be a dictionary.")
        if not isinstance(hour_traffic, int):
            raise TypeError("Invalid. Shopper traffic per hour should be an integer.")

        shopper_table = shopper_table_dict

        date = shopper_table_dict["Date"][0]
        start = self.__configuration.start_time
        start = datetime.datetime.combine(date, start)
        end = self.__configuration.end_time
        end = datetime.datetime.combine(date, end)
        traffic = (end.hour - start.hour) * hour_traffic

        shopper_table["Date"] += [date] * traffic

        day_of_week = shopper_table_dict["DayOfWeek"][0]
        shopper_table["DayOfWeek"] += [day_of_week] * traffic

        num_day_holiday = shopper_table_dict["Holiday"][0]
        shopper_table["Holiday"] += [num_day_holiday] * traffic

        sunny = shopper_table_dict["Sunny"][0]
        shopper_table["Sunny"] += [sunny] * traffic

        time_in = random_min_max(minimum=start, maximum=end, size=traffic)
        shopper_table["TimeIn"] += time_in.tolist()

        avg = self.__configuration.avg_time_spent
        time_spent = random_avg_int(avg=avg, size=traffic)
        shopper_table["TimeSpent"] += time_spent.tolist()

        senior = self.__configuration.senior_percentage
        senior = random_choice(sample_list=[True, False], probability_list=[senior, 1 - senior],
                               size=traffic)
        shopper_table["Senior"] += senior.tolist()

        return shopper_table

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated LunchRushConfiguration object.
        """
        self.__configuration = configuration


class DinnerRush:
    """Represents shopper table for a single day."""

    def __init__(self, dinner_configuration: DinnerRushConfiguration):
        """
        Initializes the DinnerRush object with a given configuration.
        :param dinner_configuration: DinnerRushConfiguration object.
        """
        if isinstance(dinner_configuration, DinnerRushConfiguration):
            self.__configuration = dinner_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a DinnerRushConfiguration object.")

    def get_day_dictionary(self, shopper_table_dict: dict, hour_traffic: int):
        """
        Returns a shopper table for a single day.
        :param shopper_table_dict: shopper table for a single day as a dictionary.
        :param hour_traffic: shopper traffic per hour as an integer.
        :return: shopper table for a single day as a dictionary.
        """
        if not isinstance(shopper_table_dict, dict):
            raise TypeError("Invalid. Shopper table dict should be a dictionary.")
        if not isinstance(hour_traffic, int):
            raise TypeError("Invalid. Shopper traffic per hour should be an integer.")

        shopper_table = shopper_table_dict

        date = shopper_table_dict["Date"][0]

        start = self.__configuration.start_time
        start = datetime.datetime.combine(date, start)
        end = self.__configuration.end_time
        end = datetime.datetime.combine(date, end)
        traffic = (end.hour - start.hour) * hour_traffic

        shopper_table["Date"] += [date] * traffic

        day_of_week = shopper_table_dict["DayOfWeek"][0]
        shopper_table["DayOfWeek"] += [day_of_week] * traffic

        num_day_holiday = shopper_table_dict["Holiday"][0]
        shopper_table["Holiday"] += [num_day_holiday] * traffic

        sunny = shopper_table_dict["Sunny"][0]
        shopper_table["Sunny"] += [sunny] * traffic


        time_in = random_min_max(minimum=start, maximum=end, size=traffic)
        shopper_table["TimeIn"] += time_in.tolist()

        avg = self.__configuration.avg_time_spent
        time_spent = random_avg_int(avg=avg, size=traffic)
        shopper_table["TimeSpent"] += time_spent.tolist()

        senior = self.__configuration.senior_percentage
        senior = random_choice(sample_list=[True, False], probability_list=[senior, 1 - senior],
                               size=traffic)
        shopper_table["Senior"] += senior.tolist()

        return shopper_table

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated DinnerRushConfiguration object.
        """
        self.__configuration = configuration


class SeniorRush:
    """Represents shopper table for a single day."""

    def __init__(self, senior_configuration: SeniorRushConfiguration):
        """
        Initializes the SeniorRush object with a given configuration.
        :param senior_configuration: SeniorRushConfiguration object.
        """
        if isinstance(senior_configuration, SeniorRushConfiguration):
            self.__configuration = senior_configuration
            self.__configuration.register_observer(self)
        else:
            raise TypeError("Invalid. The configuration should be a SeniorRushConfiguration object.")

    def get_day_dictionary(self, shopper_table_dict: dict, hour_traffic: int):
        """
        Returns a shopper table for a single day.
        :param shopper_table_dict: shopper table for a single day as a dictionary.
        :param hour_traffic: shopper traffic per hour as an integer.
        :return: shopper table for a single day as a dictionary.
        """
        if not isinstance(shopper_table_dict, dict):
            raise TypeError("Invalid. Shopper table dict should be a dictionary.")
        if not isinstance(hour_traffic, int):
            raise TypeError("Invalid. Shopper traffic per hour should be an integer.")

        day_of_week = shopper_table_dict["DayOfWeek"][0]
        if day_of_week not in day_name:
            raise AttributeError("Invalid. The day of week is invalid.")
        if day_of_week != self.__configuration.day_of_week:
            return {}

        shopper_table = shopper_table_dict

        date = shopper_table_dict["Date"][0]
        start = self.__configuration.start_time
        start = datetime.datetime.combine(date, start)
        end = self.__configuration.end_time
        end = datetime.datetime.combine(date, end)
        traffic = hour_traffic * (end.hour - start.hour)

        shopper_table["Date"] += [date] * traffic

        shopper_table["DayOfWeek"] += [day_of_week] * traffic

        num_day_holiday = shopper_table_dict["Holiday"][0]
        shopper_table["Holiday"] += [num_day_holiday] * traffic

        sunny = shopper_table_dict["Sunny"][0]
        shopper_table["Sunny"] += [sunny] * traffic

        time_in = random_min_max(minimum=start, maximum=end, size=traffic)
        shopper_table["TimeIn"] += time_in.tolist()

        mini = self.__configuration.min_time_spent
        maxi = self.__configuration.max_time_spent
        time_spent = random_min_max_int(minimum=mini, maximum=maxi, size=traffic)
        shopper_table["TimeSpent"] += time_spent.tolist()

        senior = self.__configuration.senior_percentage
        senior = random_choice(sample_list=[True, False], probability_list=[senior, 1 - senior],
                               size=traffic)
        shopper_table["Senior"] += senior.tolist()

        return shopper_table

    def update(self, configuration):
        """
        Updates the configuration with the updated configuration.
        :param configuration: updated DinnerRushConfiguration object.
        """
        self.__configuration = configuration