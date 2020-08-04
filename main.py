"""Main entry into the shopper data generator program."""
import argparse

from datetime import datetime, timedelta
from json import loads

import shopperapi.app

from configuration.holiday_modifiers import HolidayModifiers
from configuration.rush import Rush
from configuration.senior_discount import SeniorDiscount
from configuration.store_model import StoreModel
from configuration.day_modifiers import DayModifiers
from configuration.time_frame import TimeFrame

from shoppermodel.shopper_database import ShopperDatabase
from shoppermodel.shopper_table import ShopperTable



def generator_commands(parser):
    """
    Adds the optional arguments to the command line parser
    :param parser: an argparse object to add commands to
    :return: the parser the arguments were added to
    """

    # Start and End Dates
    parser.add_argument('-sd', '--start-date', default='2020-01-01', type=str,
                        help='The starting date to generate data for in format: 2019-01-01')
    parser.add_argument('-ed', '--end-date', default='2020-3-31', type=str,
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
    parser.add_argument('-wts', '--weekend-time-spent', default=60, type=int,
                        help='Average number of minutes that shoppers spend in the store on '
                             'weekends: 60')

    return parser


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

    day_modifiers = DayModifiers(args.min_time_spent, args.avg_time_spent, args.max_time_spent,
                                 args.weekend_time_spent, args.sunny_traffic_percent,
                                 args.sunny_chance_percent, args.sunny_time_spent)

    avg_shopper_traffic = {"Monday": args.mon_traffic, "Tuesday": args.tue_traffic,
                           "Wednesday": args.wed_traffic, "Thursday": args.thu_traffic,
                           "Friday": args.fri_traffic, "Saturday": args.sat_traffic,
                           "Sunday": args.sun_traffic}

    store_model = StoreModel(lunch_rush, dinner_rush, holiday_modifiers, day_modifiers,
                             senior_discount, avg_shopper_traffic, args.open_time,
                             args.close_time, args.senior_percent)

    return store_model, time_frame


def test_queries(args):
    """
    An example query of checking holiday shopper counts
    :param: the command line argument from argparse
    """
    collection = args.collection
    database = ShopperDatabase()
    database.connect_to_client()

    start = datetime(2020, 3, 5)
    end = datetime(2020, 3, 7)
    query_dict = {"Date": {"$gte": start, "$lte": end}}
    result = database.query(query_dict, collection_name=collection)
    print("\nSelected {} rows between 2020-01-01 and 2020-05-25".format(result.count()))
    print("First five rows of are:")
    for i in result.limit(5):
        print(i)

    thanksgiving = datetime(2020, 11, 26)
    week_of_start = thanksgiving - timedelta(days=6)

    holiday_week = [{"$match": {"Date": {"$gte": week_of_start,
                                         "$lte": thanksgiving}}},
                    {"$group": {"_id": "$Date",
                                "count": {"$sum": 1}}},
                    {"$sort": {"_id": -1}}]

    week_before_holiday = [{"$match": {"Date": {"$gte": week_of_start - timedelta(days=7),
                                                "$lte": thanksgiving - timedelta(days=7)}}},
                           {"$group": {"_id": "$Date",
                                       "count": {"$sum": 1}}},
                           {"$sort": {"_id": -1}}]

    print("Holiday Week Shopper Counts")
    result = database.aggregate(holiday_week, collection_name=collection)
    for i in result:
        print(i)

    print("Week Before Shopper Counts")
    result = database.aggregate(week_before_holiday, collection_name=collection)
    for i in result:
        print(i)


def run_generator(args):
    """
    Generates shopper data based on command line arguments, saves to the database and
    gives option to save to csv
    :param args: command line arguments from argparse
    :return: None
    """
    collection_name = args.collection
    path = args.path
    store_model, time_frame = create_config(args)
    shopper_table = ShopperTable(store_model, time_frame)
    shopper_table.create_table()

    # create database class and connect to the database and populate
    database = ShopperDatabase()
    database.connect_to_client()
    database.populate_shopper_database(shopper_table, collection_name)

    if path is not None:
        try:
            shopper_table.to_csv(path)
        except PermissionError:
            print("Cannot save due to PermissionError")


def query_database(args):
    """
    Connects to the database to query
    :param args:
    :return:
    """
    limit = args.limit
    database = ShopperDatabase()
    database.connect_to_client()

    running = True
    while running:
        user_query = input("Please enter a db query or enter quit to stop: ")

        if user_query == "quit" or user_query == "q":
            database.close_client()
            break

        try:
            input_dict = loads(user_query)
            print(database.query(input_dict, limit=limit))
        except ValueError:
            print("Invalid query " + user_query)


def start_api(args):
    """
    Starts the Flask app
    :param args: args from argparse
    :return: None
    """
    shopperapi.app.APP.run()


def main():
    """
    Entry point of the program
    :return: None
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='Command line arguments to generate data, '
                                            'connect to a database, start the api, or'
                                            'run test queries')

    # Generate shopper data
    generator_parser = subparsers.add_parser('generator',
                                             help='Generate shopper data and upload to database')
    generator_parser = generator_commands(generator_parser)
    generator_parser.add_argument('-col', '--collection', default='shoppers', type=str,
                                  help='The collection to save the generated shoppers to')
    generator_parser.add_argument('-p', '--path',
                                  help='The path to save a csv, will not save if no path provided')
    generator_parser.set_defaults(func=run_generator)

    # Connect to database
    db_parser = subparsers.add_parser('database', help='Connect and access the database to query')
    db_parser.add_argument('limit', default=50, type=int,
                           help='Set a limit to how many documents to receive,'
                                ' default is 50 while 0 is unlimited')
    db_parser.set_defaults(func=query_database)

    # Start api
    api_parser = subparsers.add_parser('api', help='Start and use Api')
    api_parser.set_defaults(func=start_api)

    # Run test queries
    test_parser = subparsers.add_parser('test', help='Run test queries')
    test_parser.add_argument('-col', '--collection', default='shoppers', type=str,
                             help='The collection to run the test queries on')
    test_parser.set_defaults(func=test_queries)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
