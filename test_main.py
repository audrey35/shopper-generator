"""Main entry into the shopper data generator program."""

import argparse
from datetime import datetime

from configuration.dayofweek import DayOfWeek
from configuration.holidaymodifiers import HolidayModifiers
from configuration.rush import Rush
from configuration.SeniorDiscount import SeniorDiscount
from configuration.StoreModel import StoreModel
from configuration.SunnyModifiers import SunnyModifiers
from configuration.TimeFrame import TimeFrame
from shoppermodel.shopper_database import ShopperDatabase
from shoppermodel.ShopperTable import ShopperTable


def read_commands():
    """
    Parses the commands from the command line.
    :return: parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Create a .csv of shoppers")

    # Start and End Dates
    parser.add_argument('-sd', '--start-date', default='2020-01-01', type=str,
                        help='The starting date to generate data for in format: 2019-01-01')
    parser.add_argument('-ed', '--end-date', default='2020-12-31', type=str,
                        help='The ending date to generate data for in format: 2020-12-31')

    # Open and Close Time
    parser.add_argument('-ot', '--open-time', default='06:00', type=str,
                        help='The opening time of the store: 06:00')
    parser.add_argument('-ct', '--close-time', default='21:00', type=str,
                        help='The closing time of the store: 21:00')

    # Average Traffic per Day
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

    # Lunch Rush
    parser.add_argument('-ls', '--lunch-start', default='12:00', type=str,
                        help='The time the lunch rush starts at in the store: 12:00')
    parser.add_argument('-le', '--lunch-end', default='13:00', type=str,
                        help='The time the lunch rush ends at in the store: 13:00')
    parser.add_argument('-lts', '--lunch-time-spent', default=10, type=int,
                        help='Average amount of time shoppers are spending at lunch: 10')
    parser.add_argument('-lp', '--lunch-percent', default=0.10, type=float,
                        help='Percent of shoppers coming into the store at lunchtime: 0.10')

    # Dinner Rush
    parser.add_argument('-ds', '--dinner-start', default='17:00', type=str,
                        help='The time the dinner rush starts at in the store: 12:00')
    parser.add_argument('-de', '--dinner-end', default='18:30', type=str,
                        help='The time the dinner rush ends at in the store: 13:00')
    parser.add_argument('-dts', '--dinner-time-spent', default=10, type=int,
                        help='Average amount of time shoppers are spending at dinner: 20')
    parser.add_argument('-dp', '--dinner-percent', default=0.15, type=float,
                        help='Percent of shoppers coming into the store at dinnertime: 0.15')

    # Senior Discount
    parser.add_argument('-ss', '--senior-start', default='10:00', type=str,
                        help='The time the senior discount starts at in the store: 10:00')
    parser.add_argument('-se', '--senior-end', default='12:00', type=str,
                        help='The time the senior discount end at in the store: 12:00')
    parser.add_argument('-sdp', '--senior-discount-percent', default=0.1, type=float,
                        help='Percent of seniors coming into the store on Tuesday from '
                             '10-12pm: 0.5')
    parser.add_argument('-smin', '--senior-min-time-spent', default=45, type=int,
                        help='Minimum number of minutes that senior shoppers spend in the store '
                             'during senior discount hours: 45')
    parser.add_argument('-smax', '--senior-max-time-spent', default=60, type=int,
                        help='Maximum number of minutes that senior shoppers spend in the store '
                             'during senior discount hours: 60')
    parser.add_argument('-sp', '--senior-percent', default=0.2, type=float,
                        help='Percent of seniors coming into the store: 0.2')

    # Time Spent
    parser.add_argument('-min', '--min-time-spent', default=6, type=int,
                        help='Minimum number of minutes that shoppers spend in the store: 6')
    parser.add_argument('-avg', '--avg-time-spent', default=25, type=int,
                        help='Average number of minutes that shoppers spend in the store: 25')
    parser.add_argument('-max', '--max-time-spent', default=75, type=int,
                        help='Maximum number of minutes that shoppers spend in the store: 75')

    # Holidays
    parser.add_argument('-hol', '--holiday-percent', default=0.2, type=float,
                        help='The percent decrease of shoppers due to a holiday')
    parser.add_argument('-dbh', '--day-before-holiday-percent', default=0.4, type=float,
                        help='The percent increase of shoppers due the day before a holiday')
    parser.add_argument('-wbh', '--week-before-holiday-percent', default=0.15, type=float,
                        help='The percent increase of shoppers when day is within a week '
                             'before a holiday')

    # Sunny Percentages
    parser.add_argument('-stp', '--sunny-traffic-percent', default=0.4, type=float,
                        help='The percent increase in traffic during a sunny weekend')
    parser.add_argument('-scp', '--sunny-chance-percent', default=0.3, type=float,
                        help='The percent chance that a weekend is sunny')
    parser.add_argument('-sts', '--sunny-time-spent', default=15, type=int,
                        help='The time shoppers are spending on a sunny weekend')

    # Weekend and Sunny
    parser.add_argument('-wavg', '--weekend-avg-time-spent', default=60, type=int,
                        help='Average number of minutes that shoppers spend in the store on '
                             'weekends: 60')
    parser.add_argument('-swavg', '--sunny-weekend-avg-time-spent', default=10, type=int,
                        help='Average number of minutes that shoppers spend in the store on sunny '
                             'weekends: 10')

    args = parser.parse_args()

    return args


def create_config(args):
    """
    Returns configuration objects initialized with data from parsed command line arguments.
    :param args: parsed command line arguments.
    :return: configuration objects initialized with data from parsed command line arguments.
    """

    time_frame = TimeFrame(args.start_date, args.end_date)

    lunch_rush = Rush(args.lunch_start, args.lunch_end, args.lunch_time_spent, args.lunch_percent)
    dinner_rush = Rush(args.dinner_start, args.dinner_end,
                       args.dinner_time_spent, args.dinner_percent)

    senior_discount = SeniorDiscount(args.senior_start, args.senior_end, args.senior_min_time_spent,
                                     args.senior_max_time_spent, args.senior_percent)

    holiday_modifiers = HolidayModifiers(args.holiday_percent, args.day_before_holiday_percent,
                                         args.week_before_holiday_percent)

    sunny_modifiers = SunnyModifiers(args.sunny_traffic_percent, args.sunny_chance_percent,
                                     args.sunny_time_spent)

    store_model = StoreModel(lunch_rush, dinner_rush, holiday_modifiers, sunny_modifiers,
                             senior_discount, args.open_time, args.close_time, args.senior_percent)

    mon_day_o_week = DayOfWeek("Monday", args.mon_traffic)
    tue_day_o_week = DayOfWeek("Tuesday", args.tue_traffic)
    wed_day_o_week = DayOfWeek("Wednesday", args.wed_traffic)
    thu_day_o_week = DayOfWeek("Thursday", args.thu_traffic)
    fri_day_o_week = DayOfWeek("Friday", args.fri_traffic)
    sat_day_o_week = DayOfWeek("Saturday", args.sat_traffic)
    sun_day_o_week = DayOfWeek("Sunday", args.sun_traffic)
    store_model.add_day_of_week(mon_day_o_week)
    store_model.add_day_of_week(tue_day_o_week)
    store_model.add_day_of_week(wed_day_o_week)
    store_model.add_day_of_week(thu_day_o_week)
    store_model.add_day_of_week(fri_day_o_week)
    store_model.add_day_of_week(sat_day_o_week)
    store_model.add_day_of_week(sun_day_o_week)

    return store_model, time_frame


def main():
    """Main entry into the shopper data generator program."""
    args = read_commands()
    store_model, time_frame = create_config(args)
    shopper_table = ShopperTable(store_model, time_frame)

    data_frame = shopper_table.create_table()

    # create database class and connect to the database
    database = ShopperDatabase()
    database.connect_to_client()

    col_name1 = "test_collection"
    database.populate_shopper_database(data_frame, col_name1)

    data_frame = shopper_table.create_table()

    col_name2 = "test_collection2"
    database.populate_shopper_database(data_frame, col_name2)

    # sample query and aggregation
    start = datetime(2020, 3, 5)
    end = datetime(2020, 3, 7)
    query_dict = {"Date": {"$gte": start, "$lte": end}}
    result = database.query(query_dict, collection_name=col_name1)
    print("\nSelected {} rows between 2020-01-01 and 2020-05-25".format(result.count()))
    print("First five rows of are:")
    for i in result.limit(5):
        print(i)

    agg_list = [{"$match": {"DayOfWeek": "Sunday"}},
                {"$group": {"_id": "$Date", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}]
    result = database.aggregate(agg_list, collection_name=col_name1)
    print("\nSelect Sundays and show number of rows per Date")
    for i in result:
        print(i)


if __name__ == '__main__':
    main()
