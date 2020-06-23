"""Tests the ShopperDatabase class."""

from unittest import TestCase

from shoppermodel import ShopperTable, ShopperDatabase
from test_main import read_commands, create_config


class TestShopperDatabase(TestCase):
    """
    Tests the ShopperDatabase class.
    """

    def setUp(self):
        args = read_commands()
        self.store_model, self.time_frame = create_config(args)
        self.shopper_table = ShopperTable(self.store_model, self.time_frame)

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

    def test_invalid_creation(self):
        """
        Tests TypeError is raised if invalid parameter is passed to ShopperDatabase.
        """
        with self.assertRaises(TypeError):
            ShopperDatabase(5)

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
        """
        data_frame = self.shopper_table.create_table()
        data_frame_rows = len(data_frame.index)

        database = ShopperDatabase()
        database.connect_to_client()

        col_list = database.database.list_collection_names()
        collection_name = "shoppers"
        if collection_name in col_list:
            database.delete_collection(collection_name)

        database.populate_shopper_database(data_frame)

        col_rows = database.collections[collection_name].count_documents({})
        self.assertEqual(data_frame_rows, col_rows, "Data frame rows != Collection rows")
