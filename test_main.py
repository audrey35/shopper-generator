import shoppers
import pandas as pd
import calendar
import numpy
import random
import datetime
import argparse
import Configuration

"""
Working model
"""


def generate_time_in(open_time, close_time, row_count):
    # Populate Time In
    # Evan: uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python
    times = [random.random() * (close_time - open_time) + open_time for i in range(row_count)]
    return times


def generate_percent_seniors(percent, row_count):
    percentSeniors = percent
    seniors = numpy.random.choice(a=[True, False], size=row_count, p=[percentSeniors, 1 - percentSeniors])
    return seniors.tolist()


def get_sunny(the_date, day_of_week, row_count):
    if day_of_week == 'Saturday' or day_of_week == 'Sunday':
        if 4 < the_date.month < 9:  # 70% sunny from May to August
            sunny = [numpy.random.choice(a=numpy.array([True, False]), p=[0.7, 0.3])] * row_count
        else:
            sunny = [numpy.random.choice(a=numpy.array([True, False]))] * row_count
    else:
        sunny = [False] * row_count
    return sunny


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
                        help='Average number of shoppers on Monday: 800')
    parser.add_argument('-tue', '--tue-traffic', type=int,
                        help='Average number of shoppers on Tuesday: 1000')
    parser.add_argument('-wed', '--wed-traffic', type=int,
                        help='Average number of shoppers on Wednesday: 1200')
    parser.add_argument('-thu', '--thu-traffic', type=int,
                        help='Average number of shoppers on Thursday: 900')
    parser.add_argument('-fri', '--fri-traffic', type=int,
                        help='Average number of shoppers on Friday: 2500')
    parser.add_argument('-sat', '--sat-traffic', type=int,
                        help='Average number of shoppers on Saturday: 4000')
    parser.add_argument('-sun', '--sun-traffic', type=int,
                        help='Average number of shoppers on Sunday: 5000')
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
    config = Configuration.Configuration(args.start_date, args.end_date, args.open_time, args.close_time,
                                         args.mon_traffic, args.tue_traffic, args.wed_traffic, args.thu_traffic,
                                         args.fri_traffic, args.sat_traffic, args.sun_traffic, args.min_time_spent,
                                         args.avg_time_spent, args.max_time_spent, args.senior_percent)
    return config


def main():
    import holidays

    # Possible input: list of shopper counts
    shopper_count_by_day = [800, 1000, 1200, 900, 2500, 4000, 5000]

    config = read_commands()
    # Possible input: start and end date range
    start = config.start_date
    end = config.end_date

    # Range of dates
    date_list = pd.date_range(start, end)

    # Get holiday list
    holidays = holidays.US()

    # create dictionary to fill with values
    shopper_dict = {"DayOfWeek": [], "DateTimeIn": [], "isSenior": [], "isSunny": []}

    # loop through each date
    for date in date_list:
        day_int = date.dayofweek
        day_of_week = calendar.day_name[day_int]

        num_of_shoppers = shopper_count_by_day[day_int]
        if date in holidays:
            num_of_shoppers = round(0.2 * num_of_shoppers)

        shopper_dict["DayOfWeek"] += [day_of_week] * num_of_shoppers

        # (hours, minutes)
        start_time = datetime.time(6, 0)
        end_time = datetime.time(21, 0)

        # Create a datetime object
        start_datetime = datetime.datetime.combine(date, start_time)
        end_datetime = datetime.datetime.combine(date, end_time)

        # generate time in
        shopper_dict["DateTimeIn"] += generate_time_in(start_datetime, end_datetime, num_of_shoppers)

        # add senior column
        shopper_dict["isSenior"] += generate_percent_seniors(0.2, num_of_shoppers)

        # add sunny column
        shopper_dict["isSunny"] += get_sunny(date, day_of_week, num_of_shoppers)

    df = pd.DataFrame(shopper_dict)
    print(len(df))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    print(df.head(10))
    print(df.sample(n=100))


if __name__ == '__main__':
    main()
