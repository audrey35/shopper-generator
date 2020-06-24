"""Tests the ShopperDatabase class."""
from datetime import datetime, timedelta
from unittest import TestCase

from pymongo import DESCENDING

from ShopperModel import ShopperTable, ShopperDatabase
from main import read_commands, create_config


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

        cls.database.populate_shopper_database(cls.data_frame)

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
        query_count = result.count()
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
        query_count = result.count()
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
        mongo_lunch = result.count()
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
        mongo_dinner = result.count()
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
        mongo_weekend = result.count()
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
        thanksgiving = datetime(2020, 11, 26)
        holiday_week_start = thanksgiving - timedelta(days=6)
        week_end = thanksgiving - timedelta(days=7)
        week_start = holiday_week_start - timedelta(days=7)
        holiday_week = self.data_frame.loc[(date_col >= holiday_week_start) &
                                           (date_col <= thanksgiving)]
        other_week = self.data_frame.loc[(date_col >= week_start) &
                                         (date_col <= week_end)]
        self.assertGreater(len(holiday_week), len(other_week), "holiday week should have more rows than week before")