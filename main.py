from Day import Day
from Configuration import Configuration
from TimeFrame import TimeFrame
import argparse
import pandas as pd
import numpy as np


def read_commands():
    parser = argparse.ArgumentParser(description="Create a .csv of shoppers")
    parser.add_argument('-sd', '--start-date', default='2020-01-01', type=str,
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


def main():
    # read commands and create config object
    config = read_commands()
    # create time frame object from config values
    time_frame = TimeFrame(config.start_date, config.end_date)
    # get shopper counts by day, TODO can we encapsulate this better?
    # Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    shopper_count_by_day = [config.mon_avg_traffic, config.tues_avg_traffic, config.wed_avg_traffic,
                            config.thurs_avg_traffic, config.fri_avg_traffic, config.sat_avg_traffic,
                            config.sun_avg_traffic]
    day_list = []
    for date in time_frame.dates:

        num_of_shoppers = shopper_count_by_day[date.dayofweek]

        # Check if day is in relative time to a holiday
        if time_frame.is_holiday(date):
            num_of_shoppers = round(num_of_shoppers * 0.2)
        elif time_frame.is_day_before_holiday(date):
            num_of_shoppers = round(num_of_shoppers * 1.4)
        elif time_frame.is_within_week_of_holiday(date):
            num_of_shoppers = round(num_of_shoppers * 1.15)

        if date.dayofweek in [5, 6]:
            # 70% chance that day is sunny in May through July
            if np.random.choice(a=np.array([True, False]), p=[0.7, 0.3]) and date.month in [5, 6, 7]:
                num_of_shoppers = round(num_of_shoppers * 1.4)
            # 50% change that day is sunny in other months
            elif np.random.choice(a=np.array([True, False])) and date.month not in [5, 6, 7]:
                num_of_shoppers = round(num_of_shoppers * 1.4)

        day_list.append(Day(config.open_time, config.close_time, date, num_of_shoppers, config.senior_percent))

    # create shoppers each day, append to list
    shoppers = []
    for day in day_list:
        shoppers.append(day.create_shoppers())

    # convert shoppers to dictionary
    shopper_dict = {"DateTimeIn": [], "TimeSpent": []}
    for shop_list in shoppers:
        for shopper in shop_list:
            shopper_dict["DateTimeIn"].append(shopper.time_in)
            shopper_dict["TimeSpent"].append(shopper.time_spent)

    # convert to dataframe
    df = pd.DataFrame(shopper_dict)
    df.to_csv("shoppers.csv")


if __name__ == '__main__':
    main()
