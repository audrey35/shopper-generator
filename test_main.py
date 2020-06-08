import argparse
import pandas as pd
import calendar
import holidays
import numpy
import random
import datetime

"""
Working model
"""


class Configuration:
    def __init__(self, start_date: str, end_date: str, open_time: str, close_time: str, mon_avg_traffic: int):
        # TODO: consider setting these setts and getters for each attribute
        self.start_date = start_date
        self.end_date = end_date
        self.open_time = open_time
        self.close_time = close_time
        self.mon_avg_traffic = mon_avg_traffic

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
    parser.add_argument('-mon', '--mon-traffic', type=int,
                        help='Average number of shoppers on Monday: 800', default=800)
    parser.add_argument('-tue', '--tue-traffic', type=int,
                        help='Average number of shoppers on Tuesday: 1000', default=1000)
    parser.add_argument('-wed', '--wed-traffic', type=int,
                        help='Average number of shoppers on Wednesday: 1200', default=1200)
    parser.add_argument('-thu', '--thu-traffic', type=int,
                        help='Average number of shoppers on Thursday: 900', default=900)
    parser.add_argument('-fri', '--fri-traffic', type=int,
                        help='Average number of shoppers on Friday: 2500', default=2500)
    parser.add_argument('-sat', '--sat-traffic', type=int,
                        help='Average number of shoppers on Saturday: 4000', default=4000)
    parser.add_argument('-sun', '--sun-traffic', type=int,
                        help='Average number of shoppers on Sunday: 5000', default=5000)
    parser.add_argument('-min', '--min-time-spent', type=int,
                        help='Minimum amount of time in minutes that shoppers spend in the store: 6')
    parser.add_argument('-avg', '--avg-time-spent', type=int,
                        help='Average amount of time in minutes that shoppers spend in the store: 25')
    parser.add_argument('-max', '--max-time-spent', type=int,
                        help='Maximum amount of time in minutes that shoppers spend in the store: 75')
    parser.add_argument('-sp', '--senior-percent', type=float,
                        help='Percent of seniors coming into the store: 0.2')
    args = parser.parse_args()
    print(args)
    config = Configuration(args.start_date, args.end_date, args.open_time, args.close_time, args.mon_traffic)
    return config


def generate_sunny(the_shopper_dict, the_date, the_day_of_week, row_count):
    # needs to be run after holidays
    if the_day_of_week == 'Saturday' or the_day_of_week == 'Sunday':
        if 4 < the_date.month < 9:  # 70% sunny from May to August
            sunny = [numpy.random.choice(a=numpy.array([True, False]), p=[0.7, 0.3])] * row_count
        else:
            sunny = [numpy.random.choice(a=numpy.array([True, False]))] * row_count
        if sunny[0]:
            # increase shoppers by 0.4 or 40% if the current day is a sunny weekend
            increased_row_count = round(row_count * 0.4)
            # the_shopper_dict['Date'] += [the_date] * increased_row_count
            the_shopper_dict['DayOfWeek'] += [the_day_of_week] * increased_row_count
            # shopper_dict['Holiday'] += [holiday] * increased_row_count
            sunny += [sunny[0]] * increased_row_count
    else:
        sunny = [numpy.random.choice(a=numpy.array([True, False]))] * row_count
    return sunny


def generate_percent_seniors(percent_seniors, row_count, the_day_of_week, tues_percent_seniors):
    if the_day_of_week == 'Tuesday':
        # account for 10-12pm
        seniors = numpy.random.choice(a=[True, False], size=row_count,
                                      p=[tues_percent_seniors, 1 - tues_percent_seniors])
    else:
        seniors = numpy.random.choice(a=[True, False], size=row_count, p=[percent_seniors, 1 - percent_seniors])
    return seniors.tolist()


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


def generate_time_in(open_time, close_time, row_count):
    # Populate Time In
    # Evan: uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python
    times = [random.random() * (close_time - open_time) + open_time for _ in range(row_count)]
    return times


if __name__ == '__main__':

    config = read_commands()

    print('start1',config.start_date, type(config.start_date))
    config.start_date = '2019-5-5'
    print('start2',config.start_date, type(config.start_date))

    print('end1', config.end_date, type(config.end_date))

    print(config.open_time, type(config.open_time))
    config.open_time = "5:6"

    print(config.close_time, type(config.close_time))
    config.close_time = '13:0'
    print(config.close_time, type(config.close_time))

    print(config.mon_avg_traffic, type(config.mon_avg_traffic))
    config.mon_avg_traffic = 45
    print(config.mon_avg_traffic, type(config.mon_avg_traffic))

    # Possible input: list of shopper counts
    shopper_count_by_day = [config.mon_avg_traff, config.tues_avg_traff, config.wed_avg_traff, config.thurs_avg_traff,
                            config.fri_avg_traff, config.sat_avg_traff, config.sun_avg_traff]

    # Range of dates
    date_list = pd.date_range(config.start_date, config.end_date)

    # Get holiday list
    holidays = holidays.US()

    # create dictionary to fill with values
    shopper_dict = {"DayOfWeek": [], "DateTimeIn": [], "isSenior": [], "isSunny": [], 'TimeSpent': []}

    # loop through each date
    for date in date_list:
        day_int = date.dayofweek
        day_of_week = calendar.day_name[day_int]

        num_of_shoppers = shopper_count_by_day[day_int]
        print(type(num_of_shoppers))
        if date in holidays:
            num_of_shoppers = round(0.2 * num_of_shoppers)

        elif date + datetime.timedelta(days=1) in holidays:
            num_of_shoppers = round(1.4 * num_of_shoppers)

        for i in range(2, 8):
            if date + datetime.timedelta(days=i) in holidays:
                num_of_shoppers = round(1.15 * num_of_shoppers)

        shopper_dict["DayOfWeek"] += [day_of_week] * num_of_shoppers

        # (hours, minutes)
        start_time = datetime.time(6, 0)
        end_time = datetime.time(21, 0)

        # Create a datetime object
        start_datetime = datetime.datetime.combine(date, start_time)
        end_datetime = datetime.datetime.combine(date, end_time)

        # add sunny column
        sunny_list = generate_sunny(shopper_dict, date, day_of_week, num_of_shoppers)
        shopper_dict["isSunny"] += sunny_list
        num_of_shoppers = len(sunny_list)

        # add senior column
        shopper_dict["isSenior"] += generate_percent_seniors(percent_seniors=0.2, row_count=num_of_shoppers,
                                                             the_day_of_week=day_of_week, tues_percent_seniors=0.5)

        # generate time in
        shopper_dict["DateTimeIn"] += generate_time_in(start_datetime, end_datetime, num_of_shoppers)

    # generate time spent
    is_sunny = shopper_dict['isSunny'][0]
    weekend_avg_time_spent = 60
    sunny_weekend_avg_time_spent = 10
    senior_min_time_spent = 45
    senior_max_time_spent = 60
    lunch_avg_time_spent = 10
    dinner_avg_time_spent = 20
    min_time_spent = 6
    avg_time_spent = 25
    max_time_spent = 75
    shopper_dict['TimeSpent'] = generate_time_spent(shopper_dict, weekend_avg_time_spent, sunny_weekend_avg_time_spent,
                                                    senior_min_time_spent, senior_max_time_spent,
                                                    lunch_avg_time_spent, dinner_avg_time_spent,
                                                    min_time_spent, avg_time_spent, max_time_spent)
    for i in shopper_dict.keys():
        print(i, len(shopper_dict[i]))
    df = pd.DataFrame(shopper_dict)
    df.sort_values(by=["DateTimeIn"])
    df['DateTimeIn'] = pd.to_datetime(df["DateTimeIn"].dt.strftime('%Y-%m-%d %H:%M:%S'))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df.head(10))
    print(df.sample(n=100))
