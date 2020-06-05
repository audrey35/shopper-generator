import shoppers
import pandas as pd
import calendar
import holidays
import numpy
import random
import datetime

# Populate Time In
# Evan: uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python


def generate_time_in(open_time, close_time, row_count):
    # "21/11/06 16:30", "%d/%m/%y %H:%M"
    open_time = datetime.datetime.strptime(open_time, "%m/%d/%Y %H:%M") # date and open time
    close_time = datetime.datetime.strptime(close_time, "%m/%d/%Y %H:%M") # date and close time
    # combine date with time to create datetime objects
    # account for buffer before closing time
    times = [random.random() * (close_time - open_time) + open_time for i in range(row_count)]
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
    shopper_dict = {"DayOfWeek": [], "Date": [], "TimeIn": []}

    # loop through each date
    for date in date_list:
        day_int = date.dayofweek
        day_of_week = calendar.day_name[day_int]

        num_of_shoppers = shopper_count_by_day[day_int]
        if date in holidays:
            num_of_shoppers = round(0.2 * num_of_shoppers)

        shopper_dict["DayOfWeek"] += [day_of_week] * num_of_shoppers
        shopper_dict["Date"] += [date.date()] * num_of_shoppers

        # generate time in
        shopper_dict["TimeIn"] += generate_time_in("1/1/2018 06:00", "1/1/2018 21:00", num_of_shoppers)


    df = pd.DataFrame(shopper_dict)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    pd.to_datetime(shopper_dict['TimeIn'], format='%Y-%m-%d %H:%M')
    print(df.head(10))
    print(df.sample(n=100))

