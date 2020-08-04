"""Tests the ShopperDatabase class."""
import argparse
from datetime import datetime, timedelta
from unittest import TestCase

from pymongo import DESCENDING

from configuration import *
from shoppermodel import ShopperTable, ShopperDatabase


def read_commands():
    """
    Parses the commands from the command line.
    :return: parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Create a .csv of shoppers")

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


class TestShopperDatabase(TestCase):
    """
    Tests the ShopperDatabase class.
    """

    @classmethod
    def setUpClass(cls):
        args = read_commands()
        cls.store_model, cls.time_frame = create_config(args)
        cls.shopper_table = ShopperTable(cls.store_model, cls.time_frame)
        cls.data_frame = cls.shopper_table.create_table()
        cls.data_frame["TimeIn"] = cls.data_frame["TimeIn"].astype("datetime64[s]")

        cls.database = ShopperDatabase()
        cls.database.connect_to_client()

        cls.col_list = cls.database.database.list_collection_names()
        cls.collection_name = "shoppers"
        if cls.collection_name in cls.col_list:
            cls.database.delete_collection(cls.collection_name)

        cls.database.populate_shopper_database(cls.shopper_table)

    def test_valid_creation(self):
        """
        Tests valid creation of ShopperDatabase object.
        """
        database = ShopperDatabase()
        self.assertEqual(database.uri, "", "Should be None")
        self.assertEqual(database.database_name, "", "Should be None")
        self.assertEqual(database.client, None, "Should be None")
        self.assertEqual(database.database, None, "Should be None")
        self.assertEqual(database.collections, {}, "Should be identical")

    def test_connect_to_client(self):
        """Tests connect to client works as expected."""
        database = ShopperDatabase()
        self.assertEqual(database.client, None)
        self.assertEqual(database.database, None)
        database.connect_to_client()
        self.assertEqual(database.uri, "mongodb://localhost:27017/")
        self.assertEqual(database.database_name, "shoppers_db")
        self.assertNotEqual(database.client, None)
        self.assertNotEqual(database.database, None)

    def test_populate_shopper_database(self):
        """
        Tests populate_populate_shopper_database method works as expected.
        User Story: As the technical user, I want to the the shopper
        file generated in a database
        """
        data_frame_rows = len(self.data_frame.index)
        col_rows = self.database.collections[self.collection_name].count_documents({})
        self.assertEqual(data_frame_rows, col_rows, "Data frame rows != Collection rows")

    def test_date_query(self):
        """
        Tests that query works as expected on the Date column.
        User Story: As the store owner, I can run queries to do analysis on the
        data file generated. (query)
        """
        # Test date query matches data frame results
        date_col = self.data_frame["Date"]
        start = datetime(2020, 3, 5)
        end = datetime(2020, 3, 7)
        selection = self.data_frame.loc[(date_col >= start) & (date_col <= end)]
        data_frame_count = len(selection)
        query_dict = {"Date": {"$gte": start, "$lte": end}}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        self.assertEqual(data_frame_count, result.count(), "query should yield same # of rows")
        row1_pandas = selection["Date"].tolist()[0]
        row1_query = result[0]["Date"]
        self.assertEqual(row1_pandas, row1_query)

        # Test date query with sorting matches data frame results
        pandas_sort = selection.sort_values("Date", ascending=False)
        sort_list = [("Date", DESCENDING)]
        result = self.database.query(query_dict, sort_list)
        pandas_count = len(pandas_sort)
        query_count = result.count_documents()
        self.assertEqual(pandas_count, query_count, "query should yield same # of rows")
        row1_pandas = pandas_sort["Date"].tolist()[0]
        row1_query = result[0]["Date"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

    def test_time_in_query(self):
        """
        Tests that query works as expected on the TimeIn column.
        User Story: As the store owner, I can run queries to do analysis on the
        data file generated. (query)
        """
        # Test time in query matches data frame results
        time_col = self.data_frame["TimeIn"]
        start = datetime(2020, 3, 5, 1, 0)
        end = datetime(2020, 3, 7, 15, 0)
        selection = self.data_frame.loc[(time_col >= start) & (time_col <= end)]
        data_frame_count = len(selection)
        query_dict = {"TimeIn": {"$gte": start, "$lte": end}}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        self.assertEqual(data_frame_count, result.count(), "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        # Test time in query with sorting matches data frame results
        pandas_sort = selection.sort_values("TimeIn", ascending=False)
        sort_list = [("TimeIn", DESCENDING)]
        result = self.database.query(query_dict, sort_list)
        pandas_count = len(pandas_sort)
        query_count = result.count_documents()
        self.assertEqual(pandas_count, query_count, "query should yield same # of rows")
        row1_pandas = pandas_sort["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

    def test_time_spent_query(self):
        """
        Tests that query works as expected on the TimeSpent column.
        User Story: As the store owner, I can run queries to do analysis on the
        data file generated. (query)
        """
        # Test time spent query matches data frame results
        time_col = self.data_frame["TimeSpent"]
        start = 10
        selection = self.data_frame.loc[time_col == start]
        data_frame_count = len(selection)
        query_dict = {"TimeSpent": start}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        self.assertEqual(data_frame_count, result.count(), "query should yield same # of rows")
        row1_pandas = selection["TimeSpent"].tolist()[0]
        row1_query = result[0]["TimeSpent"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

    def test_is_senior_query(self):
        """
        Tests that query works as expected on the IsSenior column.
        User Story: As the store owner, I can run queries to do analysis on the
        data file generated. (query)
        """
        # Test is senior query matches data frame results
        time_col = self.data_frame["IsSenior"]
        start = True
        selection = self.data_frame.loc[time_col == start]
        data_frame_count = len(selection)
        query_dict = {"IsSenior": start}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        self.assertEqual(data_frame_count, result.count(), "query should yield same # of rows")
        row1_pandas = selection["IsSenior"].tolist()[0]
        row1_query = result[0]["IsSenior"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        agg_list = [{"$match": {"DayOfWeek": "Sunday"}},
                    {"$group": {"_id": "$Date", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}}]
        result = self.database.aggregate(agg_list, collection_name=self.collection_name)
        print("\nSelect Sundays and show number of rows per Date")

    def test_lunch_traffic_query(self):
        """
        Tests querying for lunch traffic.
        User story: As a store owner, I want to know how much store traffic
        increases during lunch, dinner, and weekends so that I can hire
        additional staff members appropriately (query)
        """
        # Get number of shoppers before lunch
        time_col = self.data_frame["TimeIn"]
        start = datetime(2020, 3, 5, 9, 0)
        end = datetime(2020, 3, 5, 10, 0)
        selection = self.data_frame.loc[(time_col >= start) & (time_col <= end)]
        pandas_regular = len(selection)
        query_dict = {"TimeIn": {"$gte": start, "$lte": end}}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        mongo_regular = result.count()
        self.assertEqual(pandas_regular, mongo_regular, "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        # Get average number of shoppers during lunch
        time_col = self.data_frame["TimeIn"]
        start = datetime(2020, 3, 5, 12, 0)
        end = datetime(2020, 3, 5, 13, 0)
        selection = self.data_frame.loc[(time_col >= start) & (time_col <= end)]
        pandas_lunch = len(selection)
        query_dict = {"TimeIn": {"$gte": start, "$lte": end}}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        mongo_lunch = result.count_documents()
        self.assertEqual(pandas_lunch, mongo_lunch, "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        if not mongo_lunch > mongo_regular:
            print("Error. There should be more lunch shoppers then morning shoppers.")

    def test_dinner_traffic_query(self):
        """
        Tests querying for dinner traffic.
        User story: As a store owner, I want to know how much store traffic
        increases during lunch, dinner, and weekends so that I can hire
        additional staff members appropriately (query)
        """
        # Get number of shoppers before dinner
        time_col = self.data_frame["TimeIn"]
        start = datetime(2020, 3, 5, 15, 0)
        end = datetime(2020, 3, 5, 16, 30)
        selection = self.data_frame.loc[(time_col >= start) & (time_col <= end)]
        pandas_regular = len(selection)
        query_dict = {"TimeIn": {"$gte": start, "$lte": end}}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        mongo_regular = result.count()
        self.assertEqual(pandas_regular, mongo_regular, "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        # Get average number of shoppers during dinner
        time_col = self.data_frame["TimeIn"]
        start = datetime(2020, 3, 5, 17, 0)
        end = datetime(2020, 3, 5, 18, 30)
        selection = self.data_frame.loc[(time_col >= start) & (time_col <= end)]
        pandas_dinner = len(selection)
        query_dict = {"TimeIn": {"$gte": start, "$lte": end}}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        mongo_dinner = result.count_documents()
        self.assertEqual(pandas_dinner, mongo_dinner, "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        if not mongo_dinner > mongo_regular:
            print("Error. There should be more dinner shoppers then afternoon shoppers.")

    def test_weekend_traffic_query(self):
        """
        Tests querying for weekend traffic.
        User story: As a store owner, I want to know how much store traffic
        increases during lunch, dinner, and weekends so that I can hire
        additional staff members appropriately (query)
        """
        # Get number of shoppers before weekend
        day_col = self.data_frame["DayOfWeek"].str
        selection = self.data_frame.loc[day_col.contains("Friday")]
        pandas_regular = len(selection)
        query_dict = {"DayOfWeek": "Friday"}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        mongo_regular = result.count()
        self.assertEqual(pandas_regular, mongo_regular, "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        # Get average number of shoppers during weekend
        day_col = self.data_frame["DayOfWeek"].str
        selection = self.data_frame.loc[(day_col.contains("Saturday"))
                                        | (day_col.contains("Sunday"))]
        pandas_weekend = len(selection)
        query_dict = {"$or": [{"DayOfWeek": "Saturday"}, {"DayOfWeek": "Sunday"}]}
        result = self.database.query(query_dict, collection_name=self.collection_name)
        mongo_weekend = result.count_documents()
        self.assertEqual(pandas_weekend, mongo_weekend, "query should yield same # of rows")
        row1_pandas = selection["TimeIn"].tolist()[0]
        row1_query = result[0]["TimeIn"]
        self.assertEqual(row1_pandas, row1_query, "query should have the same 1st row")

        if not mongo_weekend > mongo_regular:
            print("Error. There should be more weekend shoppers then weekday shoppers.")

    def test_holiday_counts(self):
        """
        Test queries for traffic differences during a holiday
        As a store owner, I want to know how much store traffic increases
        during holiday seasons so that I can hire additional
        staff members appropriately
        """
        # get row counts for a holiday and the whole week before a holiday
        date_col = self.data_frame["Date"]
        king_day = datetime(2020, 1, 20)
        holiday_week_start = king_day - timedelta(days=6)
        week_before_end = king_day - timedelta(days=7)
        week_before_start = holiday_week_start - timedelta(days=7)
        holiday_week = self.data_frame.loc[(date_col >= holiday_week_start) &
                                           (date_col <= king_day)]
        other_week = self.data_frame.loc[(date_col >= week_before_start) &
                                         (date_col <= week_before_end)]
        self.assertGreater(len(holiday_week), len(other_week),
                           "holiday week should have more rows than week before")

        holiday_pipeline = [{"$match": {"Date": {"$gte": holiday_week_start,
                                                 "$lte": king_day}}},
                            {"$group": {"_id": "$Date",
                                        "count": {"$sum": 1}}},
                            {"$sort": {"_id": -1}}]
        week_before_holiday = [{"$match": {"Date": {"$gte": week_before_start,
                                                    "$lte": week_before_end}}},
                               {"$group": {"_id": "$Date",
                                           "count": {"$sum": 1}}},
                               {"$sort": {"_id": -1}}]
        db_holiday_result = list(self.database.aggregate(holiday_pipeline,
                                                         collection_name=self.collection_name))
        db_week_before_result = list(self.database.aggregate(week_before_holiday,
                                                             collection_name=self.collection_name))
        self.assertGreater(db_week_before_result[0]['count'], db_holiday_result[0]['count'])
        for i in range(1, 7):
            self.assertGreater(db_holiday_result[i]['count'],
                               db_week_before_result[i]['count'])
