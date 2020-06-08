import argparse
import pandas as pd
import calendar
import holidays
import numpy
import datetime

"""
Working model
"""


class Configuration:
    def __init__(self, start_date: str, end_date: str, open_time: str, close_time: str, mon_avg_traffic: int,
                 tues_avg_traffic: int, wed_avg_traffic: int, thurs_avg_traffic: int, fri_avg_traffic: int,
                 sat_avg_traffic: int, sun_avg_traffic: int, lunchtime_percent: float, dinnertime_percent: int,
                 senior_percent: float, senior_discount_percent: float,
                 min_time_spent: int, avg_time_spent: int, max_time_spent: int,
                 lunch_avg_time_spent: int, dinner_avg_time_spent: int,
                 weekend_avg_time_spent: int, sunny_weekend_avg_time_spent: int,
                 senior_min_time_spent: int, senior_max_time_spent: int):
        self.start_date = start_date
        self.end_date = end_date
        self.open_time = open_time
        self.close_time = close_time
        self.mon_avg_traffic = mon_avg_traffic
        self.tues_avg_traffic = tues_avg_traffic
        self.wed_avg_traffic = wed_avg_traffic
        self.thurs_avg_traffic = thurs_avg_traffic
        self.fri_avg_traffic = fri_avg_traffic
        self.sat_avg_traffic = sat_avg_traffic
        self.sun_avg_traffic = sun_avg_traffic
        self.lunchtime_percent = lunchtime_percent
        self.dinnertime_percent = dinnertime_percent
        self.senior_percent = senior_percent
        self.senior_discount_percent = senior_discount_percent
        self.min_time_spent = min_time_spent
        self.avg_time_spent = avg_time_spent
        self.max_time_spent = max_time_spent
        self.lunch_avg_time_spent = lunch_avg_time_spent
        self.dinner_avg_time_spent = dinner_avg_time_spent
        self.weekend_avg_time_spent = weekend_avg_time_spent
        self.sunny_weekend_avg_time_spent = sunny_weekend_avg_time_spent
        self.senior_min_time_spent = senior_min_time_spent
        self.senior_max_time_spent = senior_max_time_spent


    @property
    def start_date(self):
        """Return the start date."""
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Set the start date."""
        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise AttributeError("Invalid. Could not set the start date because the provided start date({}) is not "
                                 "a string in valid format (2018-01-01).".format(start_date))
        a_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
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
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise AttributeError("Invalid. Could not set the end date because the provided end date({}) is not "
                                 "a string in valid format (2018-01-01).".format(end_date))
        a_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        try:
            if a_end_date > self._start_date:
                self._end_date = a_end_date
            else:
                raise ValueError("Invalid. Could not set the end date because the provided end date ({}) "
                                     "should be greater than the start date({}).".format(end_date, self._start_date))
        except AttributeError:
            self._end_date = a_end_date

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
            datetime.datetime.strptime(close_time, '%H:%M').time()
        except (TypeError, ValueError):
            raise AttributeError("Invalid. Could not set the close time because the provided close time ({}) is"
                                 " not a string in valid format (21:00).".format(close_time))
        a_close_time = datetime.datetime.strptime(close_time, '%H:%M').time()
        try:
            if a_close_time > self._open_time:
                self._close_time = a_close_time
            else:
                raise ValueError("Invalid. Could not set the close time because the provided close time ({}) is"
                                 " less than the open time({}).".format(close_time, self._open_time))
        except AttributeError:
            self._close_time = a_close_time

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
            raise AttributeError("Invalid. Could not set the average traffic for Monday because the provided value "
                                 "({}) is not an integer.".format(mon_avg_traffic))
        if mon_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Monday because the value ({})"
                                 " is less than 0.".format(mon_avg_traffic))
        self._mon_avg_traffic = mon_avg_traffic

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
            raise AttributeError("Invalid. Could not set the average traffic for Tuesday because the provided value "
                                 "({}) is not an integer.".format(tues_avg_traffic))
        if tues_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Tuesday because the value ({})"
                                 " is less than 0.".format(tues_avg_traffic))
        self._tues_avg_traffic = tues_avg_traffic

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
            raise AttributeError("Invalid. Could not set the average traffic for Wednesday because the provided value "
                                 "({}) is not an integer.".format(wed_avg_traffic))
        if wed_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Wednesday because the value ({})"
                                 " is less than 0.".format(wed_avg_traffic))
        self._wed_avg_traffic = wed_avg_traffic

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
            raise AttributeError("Invalid. Could not set the average traffic for Thursday because the provided value "
                                 "({}) is not an integer.".format(thurs_avg_traffic))
        if thurs_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Thursday because the value ({})"
                                 " is less than 0.".format(thurs_avg_traffic))
        self._thurs_avg_traffic = thurs_avg_traffic

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
            raise AttributeError("Invalid. Could not set the average traffic for Friday because the provided value "
                                 "({}) is not an integer.".format(fri_avg_traffic))
        if fri_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Friday because the value ({})"
                                 " is less than 0.".format(fri_avg_traffic))
        self._fri_avg_traffic = fri_avg_traffic

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
            raise AttributeError("Invalid. Could not set the average traffic for Saturday because the provided value "
                                 "({}) is not an integer.".format(sat_avg_traffic))
        if sat_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Saturday because the value ({})"
                                 " is less than 0.".format(sat_avg_traffic))
        self._sat_avg_traffic = sat_avg_traffic

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
            raise AttributeError("Invalid. Could not set the average traffic for Sunday because the provided value "
                                 "({}) is not an integer.".format(sun_avg_traffic))
        if sun_avg_traffic < 0:
            raise AttributeError("Invalid. Could not set the average traffic for Sunday because the value ({})"
                                 " is less than 0.".format(sun_avg_traffic))
        self._sun_avg_traffic = sun_avg_traffic

    @property
    def lunchtime_percent(self):
        """Return the percentage of shoppers coming in at lunchtime."""
        return self._lunchtime_percent

    @lunchtime_percent.setter
    def lunchtime_percent(self, lunchtime_percent):
        """Set the percentage of shoppers coming in at lunchtime."""
        try:
            lunchtime_percent = float(lunchtime_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at lunchtime"
                                 " because the provided value ({}) is not a float.".format(lunchtime_percent))
        if lunchtime_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at lunchtime"
                                 " because the value ({}) is less than 0.".format(lunchtime_percent))
        self._lunchtime_percent = lunchtime_percent

    @property
    def dinnertime_percent(self):
        """Return the percentage of shoppers coming in at dinnertime."""
        return self._dinnertime_percent

    @dinnertime_percent.setter
    def dinnertime_percent(self, dinnertime_percent):
        """Set the percentage of shoppers coming in at dinnertime."""
        try:
            dinnertime_percent = float(dinnertime_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at dinnertime"
                                 " because the provided value ({}) is not a float.".format(dinnertime_percent))
        if dinnertime_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of shoppers coming in at dinnertime"
                                 " because the value ({}) is less than 0.".format(dinnertime_percent))
        self._dinnertime_percent = dinnertime_percent

    @property
    def senior_percent(self):
        """Return the percentage of seniors coming in at any given hour."""
        return self._senior_percent

    @senior_percent.setter
    def senior_percent(self, senior_percent):
        """Set the percentage of seniors coming in at any given hour."""
        try:
            senior_percent = float(senior_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in at any given hour"
                                 " because the provided value ({}) is not a float.".format(senior_percent))
        if senior_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in at any given hour"
                                 " because the value ({}) is less than 0.".format(senior_percent))
        self._senior_percent = senior_percent

    @property
    def senior_discount_percent(self):
        """Return the percentage of seniors coming in on Tuesday 10-12pm."""
        return self._senior_discount_percent

    @senior_discount_percent.setter
    def senior_discount_percent(self, senior_discount_percent):
        """Set the percentage of seniors coming in on Tuesday 10-12pm."""
        try:
            senior_discount_percent = float(senior_discount_percent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in  on Tuesday 10-12pm"
                                 " because the provided value ({}) is not a float.".format(senior_discount_percent))
        if senior_discount_percent < 0:
            raise AttributeError("Invalid. Could not set the percentage of seniors coming in on Tuesday 10-12pm"
                                 " because the value ({}) is less than 0.".format(senior_discount_percent))
        self._senior_discount_percent = senior_discount_percent

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
            raise AttributeError("Invalid. Could not set the minimum time spent because the provided value "
                                 "({}) is not an integer.".format(min_time_spent))
        if min_time_spent < 0:
            raise AttributeError("Invalid. Could not set the minimum time spent because the value ({})"
                                 " is less than 0.".format(min_time_spent))
        self._min_time_spent = min_time_spent

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
            raise AttributeError("Invalid. Could not set the average time spent because the provided value "
                                 "({}) is not an integer.".format(avg_time_spent))
        if avg_time_spent < 0:
            raise AttributeError("Invalid. Could not set the average time spent because the value ({})"
                                 " is less than 0.".format(avg_time_spent))
        self._avg_time_spent = avg_time_spent

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
            raise AttributeError("Invalid. Could not set the maximum time spent because the provided value "
                                 "({}) is not an integer.".format(max_time_spent))
        if max_time_spent < 0:
            raise AttributeError("Invalid. Could not set the maximum time spent because the value ({})"
                                 " is less than 0.".format(max_time_spent))
        self._max_time_spent = max_time_spent

    @property
    def lunch_avg_time_spent(self):
        """Return the average time a shopper spends in the store at lunchtime."""
        return self._lunch_avg_time_spent

    @lunch_avg_time_spent.setter
    def lunch_avg_time_spent(self, lunch_avg_time_spent):
        """Set the average time a shopper spends in the store at lunchtime."""
        try:
            lunch_avg_time_spent = float(lunch_avg_time_spent)
        except ValueError:
            raise AttributeError(
                "Invalid. Could not set the the average time a shopper spends in the store at lunchtime"
                " because the provided value ({}) is not a float.".format(lunch_avg_time_spent))
        if lunch_avg_time_spent < 0:
            raise AttributeError("Invalid. Could not set the average time a shopper spends in the store at lunchtime"
                                 " because the value ({}) is less than 0.".format(lunch_avg_time_spent))
        self._lunch_avg_time_spent = lunch_avg_time_spent

    @property
    def dinner_avg_time_spent(self):
        """Return the average time a shopper spends in the store at dinnertime."""
        return self._dinner_avg_time_spent

    @dinner_avg_time_spent.setter
    def dinner_avg_time_spent(self, dinner_avg_time_spent):
        """Set the average time a shopper spends in the store at dinnertime."""
        try:
            dinner_avg_time_spent = float(dinner_avg_time_spent)
        except ValueError:
            raise AttributeError(
                "Invalid. Could not set the the average time a shopper spends in the store at dinnertime"
                " because the provided value ({}) is not a float.".format(dinner_avg_time_spent))
        if dinner_avg_time_spent < 0:
            raise AttributeError("Invalid. Could not set the average time a shopper spends in the store at dinnertime"
                                 " because the value ({}) is less than 0.".format(dinner_avg_time_spent))
        self._dinner_avg_time_spent = dinner_avg_time_spent

    @property
    def senior_min_time_spent(self):
        """Return the minimum time a senior shopper spends in the store during senior discount hours."""
        return self._senior_min_time_spent

    @senior_min_time_spent.setter
    def senior_min_time_spent(self, senior_min_time_spent):
        """Set the minimum time a senior shopper spends in the store during senior discount hours."""
        try:
            senior_min_time_spent = float(senior_min_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the the minimum time a senior shopper spends in the store "
                                 "during senior discount hours because the provided value ({}) is "
                                 "not a float.".format(senior_min_time_spent))
        if senior_min_time_spent < 0:
            raise AttributeError("Invalid. Could not set the minimum time a senior shopper spends in the store during "
                                 "senior discount hours because the value ({}) is "
                                 "less than 0.".format(senior_min_time_spent))
        self._senior_min_time_spent = senior_min_time_spent

    @property
    def senior_max_time_spent(self):
        """Return the maximum time a senior shopper spends in the store during senior discount hours."""
        return self._senior_max_time_spent

    @senior_max_time_spent.setter
    def senior_max_time_spent(self, senior_max_time_spent):
        """Set the maximum time a senior shopper spends in the store during senior discount hours."""
        try:
            senior_max_time_spent = float(senior_max_time_spent)
        except ValueError:
            raise AttributeError("Invalid. Could not set the the maximum time a senior shopper spends in the store "
                                 "during senior discount hours because the provided value ({}) is "
                                 "not a float.".format(senior_max_time_spent))
        if senior_max_time_spent < 0:
            raise AttributeError("Invalid. Could not set the maximum time a senior shopper spends in the store during "
                                 "senior discount hours because the value ({}) is "
                                 "less than 0.".format(senior_max_time_spent))
        self._senior_max_time_spent = senior_max_time_spent


def read_commands():
    parser = argparse.ArgumentParser(description="Create a .csv of shoppers")
    parser.add_argument('-sd', '--start-date', default='2019-01-01', type=str,
                        help='The starting date to generate data for in format: 2019-01-01')
    parser.add_argument('-ed', '--end-date', default='2020-12-31', type=str,
                        help='The ending date to generate data for in format: 2020-12-31')
    parser.add_argument('-ot', '--open-time', default='06:00', type=str,
                        help='The opening time of the store: 06:00')
    parser.add_argument('-ct', '--close-time', default='21:00', type=str,
                        help='The closing time of the store: 21:00')
    parser.add_argument('-mon', '--mon-traffic', default=800, type=int,
                        help='Average number of shoppers on Monday: 800')
    parser.add_argument('-tue', '--tue-traffic', default=1000, type=int,
                        help='Average number of shoppers on Tuesday: 1000')
    parser.add_argument('-wed', '--wed-traffic', default=1200, type=int,
                        help='Average number of shoppers on Wednesday: 1200')
    parser.add_argument('-thu', '--thu-traffic', default=900, type=int,
                        help='Average number of shoppers on Thursday: 900')
    parser.add_argument('-fri', '--fri-traffic', default=2500, type=int,
                        help='Average number of shoppers on Friday: 2500')
    parser.add_argument('-sat', '--sat-traffic', default=4000, type=int,
                        help='Average number of shoppers on Saturday: 4000')
    parser.add_argument('-sun', '--sun-traffic', default=5000, type=int,
                        help='Average number of shoppers on Sunday: 5000')
    parser.add_argument('-lp', '--lunchtime-percent', default=0.05, type=float,
                        help='Percent of shoppers coming into the store at lunchtime: 0.05')
    parser.add_argument('-dp', '--dinnertime-percent', default=0.05, type=float,
                        help='Percent of shoppers coming into the store at dinnertime: 0.05')
    parser.add_argument('-sp', '--senior-percent', default=0.2, type=float,
                        help='Percent of seniors coming into the store: 0.2')
    parser.add_argument('-sdp', '--senior-discount-percent', default=0.5, type=float,
                        help='Percent of seniors coming into the store on Tuesday from 10-12pm: 0.5')
    parser.add_argument('-min', '--min-time-spent', default=6, type=int,
                        help='Minimum number of minutes that shoppers spend in the store: 6')
    parser.add_argument('-avg', '--avg-time-spent', default=25, type=int,
                        help='Average number of minutes that shoppers spend in the store: 25')
    parser.add_argument('-max', '--max-time-spent', default=75, type=int,
                        help='Maximum number of minutes that shoppers spend in the store: 75')
    parser.add_argument('-lavg', '--lunchtime-avg-time-spent', default=10, type=int,
                        help='Average number of minutes that shoppers spend in the store during lunchtime: 10')
    parser.add_argument('-davg', '--dinnertime-avg-time-spent', default=20, type=int,
                        help='Average number of minutes that shoppers spend in the store during dinnertime: 20')
    parser.add_argument('-wavg', '--weekend-avg-time-spent', default=60, type=int,
                        help='Average number of minutes that shoppers spend in the store on weekends: 60')
    parser.add_argument('-swavg', '--sunny-weekend-avg-time-spent', default=10, type=int,
                        help='Average number of minutes that shoppers spend in the store on sunny weekends: 10')
    parser.add_argument('-smin', '--senior-min-time-spent', default=45, type=int,
                        help='Minimum number of minutes that senior shoppers spend in the store during senior '
                             'discount hours: 45')
    parser.add_argument('-smax', '--senior-max-time-spent', default=60, type=int,
                        help='Maximum number of minutes that senior shoppers spend in the store during senior '
                             'discount hours: 60')


    args = parser.parse_args()
    print(args)
    config = Configuration(args.start_date, args.end_date, args.open_time, args.close_time,
                           args.mon_traffic, args.tue_traffic, args.wed_traffic, args.thu_traffic,
                           args.fri_traffic, args.sat_traffic, args.sun_traffic,
                           args.lunchtime_percent, args.dinnertime_percent,
                           args.senior_percent, args.senior_discount_percent,
                           args.min_time_spent, args.avg_time_spent, args.max_time_spent,
                           args.lunchtime_avg_time_spent, args.dinnertime_avg_time_spent,
                           args.weekend_avg_time_spent, args.sunny_weekend_avg_time_spent,
                           args.senior_min_time_spent, args.senior_max_time_spent)
    return config


def generate_sunny(the_date, the_day_of_week, row_count):
    # needs to be run after dayofweek and holidays, but before anything else
    if the_day_of_week == 'Saturday' or the_day_of_week == 'Sunday':
        if 4 < the_date.month < 9:  # 70% chance of being a sunny day if day is between May and August
            sunny = [numpy.random.choice(a=numpy.array([True, False]), p=[0.7, 0.3])] * row_count
        else:  # 50% chance of being a sunny day if the day is of any other months
            sunny = [numpy.random.choice(a=numpy.array([True, False]))] * row_count
        if sunny[0]:
            # increase shoppers by 0.4 or 40% if the current day is a sunny weekend
            sunny += [sunny[0]] * round(row_count * 0.4)
    else:  # not a weekend, no changes to shopper count
        sunny = [numpy.random.choice(a=numpy.array([True, False]))] * row_count
    return sunny


def generate_percent_seniors(time_in_list, day_of_week, row_count, percent_seniors, tues_percent_seniors):
    # needs to be run after running time in
    # Apply percentage of seniors at any given time
    values = numpy.random.choice(a=numpy.array([True, False]), p=[percent_seniors, 1 - percent_seniors], size=row_count)
    seniors = values.tolist()
    # Apply percentage of seniors at senior discount time
    if day_of_week == 'Tuesday':
        subset_dict = {'isSenior': seniors, 'DateTimeIn': time_in_list}
        tbl = pd.DataFrame(subset_dict)
        hour = tbl['DateTimeIn'].dt.hour
        minute = tbl['DateTimeIn'].dt.minute
        sel = tbl.loc[(hour == 10) | (hour == 11) | ((hour == 12) & (minute == 0))]
        sel_values = numpy.random.choice(a=numpy.array([True, False]),
                                      p=[tues_percent_seniors, 1 - tues_percent_seniors], size=len(sel.index))
        tbl.loc[(hour == 10) | (hour == 11) | ((hour == 12) & (minute == 0)), 'isSenior'] = sel_values
        seniors = tbl['isSenior'].tolist()
    return seniors


def generate_time_spent(the_shopper_dict: dict,
                        the_weekend_avg_time_spent: int, the_sunny_weekend_avg_time_spent: int,
                        the_senior_min_time_spent: int, the_senior_max_time_spent: int,
                        the_lunch_avg_time_spent: int, the_dinner_avg_time_spent: int,
                        the_min_time_spent: int, the_avg_time_spent: int, the_max_time_spent: int):
    # Apply general time spent
    length = len(the_shopper_dict['DayOfWeek'])
    values = numpy.random.normal(loc=the_avg_time_spent, scale=round(the_avg_time_spent / 2), size=length)
    values = numpy.round(values).astype(int)
    # numpy.clip is used to remove values less than min_minute_spent or greater than max_minute_spent
    # without changing the mean of the numpy array
    # numpy.clip source: https://stackoverflow.com/a/44603019
    values = numpy.clip(values, the_min_time_spent, the_max_time_spent)
    the_shopper_dict['TimeSpent'] = values
    tbl = pd.DataFrame(the_shopper_dict)
    print('general', length)
    print(tbl.sample(n=5))
    hour = tbl['DateTimeIn'].dt.hour
    minute = tbl['DateTimeIn'].dt.minute
    day_of_week_col = tbl['DayOfWeek'].str
    sunny_col = tbl['isSunny']
    # Select Tuesday 10-12pm
    sel = tbl.loc[(tbl['DayOfWeek'].str.contains('Tuesday')) &
                  ((hour == 10) | (hour == 11) | ((hour == 12) & (minute == 0))) & tbl['isSenior'] == True]
    sel_values = numpy.random.rand(len(sel.index))
    sel_values = sel_values * (the_senior_max_time_spent - the_senior_min_time_spent) + the_senior_min_time_spent
    sel_values = numpy.round(sel_values).astype(int)
    tbl.loc[(tbl['DayOfWeek'].str.contains('Tuesday')) &
            ((hour == 10) | (hour == 11) | ((hour == 12) & (minute == 0))) &
            tbl['isSenior'] == True, 'TimeSpent'] = sel_values
    sel = tbl.loc[(tbl['DayOfWeek'].str.contains('Tuesday')) &
                  ((hour == 10) | (hour == 11) | ((hour == 12) & (minute == 0))) & tbl['isSenior'] == True]
    print('tuesday', len(sel.index))
    print(sel.head(5))
    # Select lunchtime 12-1pm
    sel = tbl.loc[(hour == 12) | ((hour == 13) & (minute == 0))]
    sel_values = numpy.random.normal(loc=the_lunch_avg_time_spent, size=len(sel.index))
    sel_values = numpy.round(sel_values).astype(int)
    tbl.loc[(hour == 12) | ((hour == 13) & (minute == 0)), 'TimeSpent'] = sel_values
    sel = tbl.loc[(hour == 12) | ((hour == 13) & (minute == 0))]
    print('lunch time', len(sel.index))
    print(sel.sample(n=5))
    # Select dinnertime 5-6:30pm
    sel = tbl.loc[(hour == 17) | ((hour == 18) & (minute <= 30))]
    sel_values = numpy.random.normal(loc=the_dinner_avg_time_spent, size=len(sel.index))
    sel_values = numpy.round(sel_values).astype(int)
    tbl.loc[(hour == 17) | ((hour == 18) & (minute <= 30)), 'TimeSpent'] = sel_values
    sel = tbl.loc[(hour == 17) | ((hour == 18) & (minute <= 30))]
    print('dinnertime', len(sel.index))
    print(sel.sample(n=5))
    # Select sunny weekends
    sel = tbl.loc[((day_of_week_col.contains('Saturday')) | (day_of_week_col.contains('Sunday'))) &
                  (sunny_col == True)]
    sel_values = numpy.random.normal(loc=the_sunny_weekend_avg_time_spent, size=len(sel.index))
    sel_values = numpy.round(sel_values).astype(int)

    tbl.loc[((day_of_week_col.contains('Saturday')) | (day_of_week_col.contains('Sunday'))) &
            (sunny_col == True), 'TimeSpent'] = sel_values
    sel = tbl.loc[((day_of_week_col.contains('Saturday')) | (day_of_week_col.contains('Sunday'))) &
                  (sunny_col == True)]
    print('sunny weekend', len(sel.index))
    print(sel.sample(n=5))
    # Select regular weekends
    sel = tbl.loc[((day_of_week_col.contains('Saturday')) | (day_of_week_col.contains('Sunday'))) &
                  (sunny_col == False)]
    sel_values = numpy.random.normal(loc=the_weekend_avg_time_spent, size=len(sel.index))
    sel_values = numpy.round(sel_values).astype(int)
    tbl.loc[((day_of_week_col.contains('Saturday')) | (day_of_week_col.contains('Sunday'))) &
            (sunny_col == False), 'TimeSpent'] = sel_values
    sel = tbl.loc[((day_of_week_col.contains('Saturday')) | (day_of_week_col.contains('Sunday'))) &
                  (sunny_col == False)]
    print('regular weekend', len(sel.index))
    print(sel.sample(n=5))
    time_spent = tbl['TimeSpent'].tolist()
    del tbl
    return time_spent


def generate_time_in(date, open_time, close_time, row_count, lunchtime_percent_increase, dinnertime_percent_increase):
    # Populate Time In
    # Evan: uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python
    times = numpy.random.random(row_count) * (close_time - open_time) + open_time
    # add lunchtime % increase in shopper count
    lunch_start_time = datetime.datetime.combine(date, datetime.time(12, 0))
    lunch_end_time = datetime.datetime.combine(date, datetime.time(1, 0))
    lunch = numpy.random.random(size=round(row_count * (1 + lunchtime_percent_increase)))
    lunch = lunch * (lunch_end_time - lunch_start_time) + lunch_start_time
    # add dinnertime % increase in shopper count
    dinner_start_time = datetime.datetime.combine(date, datetime.time(5, 0))
    dinner_end_time = datetime.datetime.combine(date, datetime.time(6, 30))
    dinner = numpy.random.random(size=round(row_count * (1 + dinnertime_percent_increase)))
    dinner = dinner * (dinner_end_time - dinner_start_time) + dinner_start_time
    times = times.tolist() + lunch.tolist() + dinner.tolist()
    return times


if __name__ == '__main__':

    config = read_commands()

    # Possible input: list of shopper counts
    shopper_count_by_day = [config.mon_avg_traffic, config.tues_avg_traffic, config.wed_avg_traffic,
                            config.thurs_avg_traffic, config.fri_avg_traffic, config.sat_avg_traffic,
                            config.sun_avg_traffic]

    # Range of dates
    date_list = pd.date_range(config.start_date, config.end_date)

    # Get holiday list
    holidays = holidays.US()

    # create dictionary to fill with values
    shopper_dict = {"DayOfWeek": [], "DateTimeIn": [], "isSunny": [], "isSenior": []}

    # variables from config
    open_time = config.open_time
    close_time = config.close_time
    lunchtime_percent = config.lunchtime_percent
    dinnertime_percent = config.dinnertime_percent
    senior_percent = config.senior_percent
    senior_discount_percent = config.senior_discount_percent
    min_time_spent = config.min_time_spent
    avg_time_spent = config.avg_time_spent
    max_time_spent = config.max_time_spent
    lunch_avg_time_spent = config.lunch_avg_time_spent
    dinner_avg_time_spent = config.dinner_avg_time_spent
    weekend_avg_time_spent = config.weekend_avg_time_spent
    sunny_weekend_avg_time_spent = config.sunny_weekend_avg_time_spent
    senior_min_time_spent = config.senior_min_time_spent
    senior_max_time_spent = config.senior_max_time_spent


    # loop through each date
    for date in date_list:
        day_int = date.dayofweek
        day_of_week = calendar.day_name[day_int]

        num_of_shoppers = shopper_count_by_day[day_int]
        if date in holidays:
            num_of_shoppers = round(0.2 * num_of_shoppers)

        elif date + datetime.timedelta(days=1) in holidays:
            num_of_shoppers = round(1.4 * num_of_shoppers)

        for i in range(2, 8):
            if date + datetime.timedelta(days=i) in holidays:
                num_of_shoppers = round(1.15 * num_of_shoppers)

        # Create a datetime object
        open_datetime = datetime.datetime.combine(date, open_time)
        close_datetime = datetime.datetime.combine(date, close_time)

        # get sunny column length
        sunny_list = generate_sunny(date, day_of_week, num_of_shoppers)

        num_of_shoppers = len(sunny_list)

        # generate time in
        time_list = generate_time_in(date, open_datetime, close_datetime, num_of_shoppers,
                                     lunchtime_percent, dinnertime_percent)
        num_of_shoppers = len(time_list)

        # update sunny to new num_of_shoppers
        diff = len(time_list) - len(sunny_list)
        if diff > 0:
            sunny_list += [sunny_list[0]] * diff

        # generate seniors
        seniors = generate_percent_seniors(time_list, day_of_week, num_of_shoppers,
                                           senior_percent, senior_discount_percent)

        shopper_dict["DayOfWeek"] += [day_of_week] * num_of_shoppers
        shopper_dict["DateTimeIn"] += time_list
        shopper_dict["isSunny"] += sunny_list
        shopper_dict['isSenior'] += seniors

    # generate time spent
    shopper_dict['TimeSpent'] = generate_time_spent(shopper_dict, weekend_avg_time_spent, sunny_weekend_avg_time_spent,
                                                    senior_min_time_spent, senior_max_time_spent,
                                                    lunch_avg_time_spent, dinner_avg_time_spent,
                                                    min_time_spent, avg_time_spent, max_time_spent)
    df = pd.DataFrame(shopper_dict)
    df.sort_values(by=["DateTimeIn"])
    df['DateTimeIn'] = pd.to_datetime(df["DateTimeIn"].dt.strftime('%Y-%m-%d %H:%M:%S'))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df.head(10))
    print(df.sample(n=100))
