"""Represents the MongoDB database for the shopper data."""

import pandas
import pymongo


class ShopperDatabase:
    """
    Represents the MongoDB database for the shopper data.
    """

    def __init__(self):
        """
        Instantiates the ShopperDatabase object.
        """
        self.uri = ""
        self.database_name = ""
        self.client = None
        self.database = None
        self.collections = {}

    def connect_to_client(self, uri="mongodb://localhost:27017/", database_name="shoppers_db"):
        """
        Connects to the MongoDB client and database.
        :param uri: URI for the MongoDB.
        :param database_name: name of the MongoDB database to connect to.
        """
        if self.client is None:
            self.uri = uri
            self.database_name = database_name
            self.client = pymongo.MongoClient(uri)
            # Connect to a database (MongoDB will create, if it doesn't exist)
            self.database = self.client[database_name]
        else:
            raise ConnectionError('Connection to client already established.')

    def close_client(self):
        """Closes the connection to the MongoDB client."""
        if self.client is not None:
            self.client = self.client.close()
            del self.database
            del self.collections
        else:
            raise ConnectionError('No client connection established.')

    def populate_shopper_database(self, data_frame, collection_name="shoppers"):
        """
        Populates the shopper database with the given pandas data frame
        by converting the data frame into a records-based dictionary and
        inserting it into a MongoDB database collection.
        :param data_frame: pandas data frame containing the data to pull
        into the MongoDB database. This method will overwrite the collection if it exists.
        :param collection_name: a unique name for the collection to be created.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection already exists in the database.
        """
        if self.client is None and self.uri != "" and self.database_name != "":
            self.connect_to_client(self.uri, self.database_name)
        elif self.client is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")

        col_list = self.database.list_collection_names()
        if collection_name in col_list:
            self.delete_collection(collection_name)

        # Create/Connect to a collection
        collection = self.database[collection_name]

        # create ID column for use in MongoDB
        data_frame["_id"] = data_frame["ShopperId"]

        # convert to datetime for MongoDB
        data_frame["Date"] = pandas.to_datetime(data_frame["Date"])
        data_frame["TimeIn"] = pandas.to_datetime(data_frame["TimeIn"])

        # convert pandas data frame to dictionary
        data = data_frame.to_dict("records")

        # add data to the database
        collection.insert_many(data)

        # Add collection to the dictionary of collections
        self.collections[collection_name] = collection

    def populate_shopper_database_from_csv(self, csv_path="shoppers.csv",
                                           collection_name="shoppers"):
        """
        Populates the shopper database with the given csv
        by converting the csv into a pandas data frame,
        then converting the data frame into a records-based dictionary
        and inserting it into a MongoDB database collection.
        :param csv_path: path to the csv file with data to pull
        into the MongoDB database.
        :param collection_name: a unique name for the collection to be created.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection already exists in the database.
        """
        # Load the csv file into a pandas data frame.
        data = pandas.read_csv(csv_path, encoding="ISO-8859-1")
        self.populate_shopper_database(data, collection_name)

    def query(self, query_dict: dict, sort_list=None, collection_name="shoppers"):
        """
        Returns the results of a query.
        :param query_dict: a dictionary of the query statement.
        :param sort_list: a list of fields to sort by (optional).
        :param collection_name: name of the collection to query on.
        :return: resulting query object.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection does not exist in the database.
        """
        collection = self.__verify_connections(collection_name)

        if isinstance(sort_list, list) or sort_list is None:
            output = collection.find(query_dict)
        else:
            output = collection.find(query_dict).sort(sort_list)
        return output

    def aggregate(self, agg_list: list, collection_name="shoppers"):
        """
        Returns the results of an aggregation.
        :param agg_list: a list of the aggregation statement.
        :param collection_name: name of the collection to aggregate.
        :return: resulting aggregation object.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection does not exist in the database.
        """
        collection = self.__verify_connections(collection_name)

        return collection.aggregate(agg_list)

    def get_database_collection(self, collection_name="shoppers"):
        """
        Returns the connections to the MongoDB database and collection as a tuple.
        :return: the connections to the MongoDB database and collection as a tuple.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection does not exist in the database.
        """
        collection = self.__verify_connections(collection_name)

        return self.database, collection

    def delete_collection(self, collection_name):
        """
        Deletes a collection from the MongoDB database.
        :param collection_name:
        ConnectionError: If connect_to_client was not executed prior to running this method.
        """
        if self.client is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")
        # remove collection from collections list
        if collection_name in self.collections:
            self.collections.pop(collection_name)
        # delete collection from the database
        col_list = self.database.list_collection_names()
        if collection_name in col_list:
            self.database[collection_name].drop()

    def __verify_connections(self, collection_name):
        """
        Verifies that a connection to a MongoDB database and collection has been made.
        :param collection_name: name of the collection being verified.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection does not exist in the database.
        """
        if self.client is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")
        if collection_name not in self.collections:
            col_list = self.database.list_collection_names()
            if collection_name in col_list:
                collection = self.database[collection_name]
                self.collections[collection_name] = collection
            else:
                msg = "Collection does not exist. Please use populate shopper database first."
                raise ValueError(msg)
        else:
            collection = self.collections[collection_name]
        return collection
