import shoppers
import pandas as pd
import calendar
import holidays
import numpy
import random
import datetime

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
    seniors = numpy.random.choice(a=[True, False], size=row_count, p=[percentSeniors, 1-percentSeniors])
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


if __name__ == '__main__':

    # Possible input: list of shopper counts
    shopper_count_by_day = [800, 1000, 1200, 900, 2500, 4000, 5000]

    # Possible input: start and end date range
    start = '2019-01-01'
    end = '2020-12-31'

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
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    print(df.head(10))
    print(df.sample(n=100))

