"""Tests the ShopperDatabase class."""

from unittest import TestCase

from ShopperModel import ShopperTable, ShopperDatabase
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
        db = ShopperDatabase()
        self.assertEqual(db.uri, "", "Should be None")
        self.assertEqual(db.database_name, "", "Should be None")
        self.assertEqual(db.client, None, "Should be None")
        self.assertEqual(db.database, None, "Should be None")
        self.assertEqual(db.collections, {}, "Should be identical")

    def test_invalid_creation(self):
        """
        Tests TypeError is raised if invalid parameter is passed to ShopperDatabase.
        """
        with self.assertRaises(TypeError):
            ShopperDatabase(5)

    def test_connect_to_client(self):
        """Tests connect to client works as expected."""
        db = ShopperDatabase()
        self.assertEqual(db.client, None)
        self.assertEqual(db.database, None)
        db.connect_to_client()
        self.assertEqual(db.uri, "mongodb://localhost:27017/")
        self.assertEqual(db.database_name, "shoppers_db")
        self.assertNotEqual(db.client, None)
        self.assertNotEqual(db.database, None)

    def test_populate_shopper_database(self):
        """
        Tests populate_populate_shopper_database method works as expected.
        """
        data_frame = self.shopper_table.create_table()
        data_frame_rows = len(data_frame.index)

        db = ShopperDatabase()
        db.connect_to_client()

        col_list = db.database.list_collection_names()
        collection_name = "shoppers"
        if collection_name in col_list:
            db.delete_collection(collection_name)

        db.populate_shopper_database(data_frame)

        col_rows = db.collections[collection_name].count_documents({})
        self.assertEqual(data_frame_rows, col_rows, "Data frame rows != Collection rows")


