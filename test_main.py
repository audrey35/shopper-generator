import pandas as pd
import calendar
import holidays
import numpy
import random
import datetime

"""
Working model
"""


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
        sunny = [False] * row_count
    return sunny


def generate_percent_seniors(percent_seniors, row_count, the_day_of_week, tues_percent_seniors):
    if the_day_of_week == 'Tuesday':
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
    shopper_dict = {"DayOfWeek": [], "DateTimeIn": [], "isSenior": [], "isSunny": [], 'TimeSpent': []}

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
    df['DateTimeIn'] = pd.to_datetime(df["DateTimeIn"].dt.strftime('%Y-%m-%d %H:%M'))
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df.head(10))
    print(df.sample(n=100))
