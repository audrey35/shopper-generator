import pandas
import pymongo

from ShopperModel import Configuration


class ShopperDatabase(object):
    """
    Represents the MongoDB database for the shopper data.
    """
    def __init__(self, configuration):
        """
        Instantiates the ShopperDatabase object by taking
         a Configuration object with specified parameters from the user.
        :param configuration: a Configuration object.
        """
        if type(configuration) != Configuration:
            raise TypeError("TypeError. Please provide a Configuration object.")
        self.configuration = configuration
        self.database = None
        self.collection = None

    def populate_shopper_database(self, data_frame):
        """
        Populates the shopper database with the given pandas data frame
        by converting the data frame into a records-based dictionary and
        inserting it into a MongoDB database collection.
        :param data_frame: pandas data frame containing the data to pull
        into the MongoDB database. The name of the database and collection
        comes from the configuration class (parameters are edited in command line).
        :return: Nothing.
        """
        # TODO: parameters below should have the defaults set and need to come from config
        database_name = "shoppers_db"
        collection_name = "shoppers"

        # Create a MongoClient Object and specify a connection URL
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # Connect to a database (MongoDB will create, if it doesn't exist)
        self.database = client[database_name]

        # Delete "shoppers" collection if it exists (allows reruns)
        col_list = self.database.list_collection_names()
        if collection_name in col_list:
            self.database[collection_name].drop()

        # Create a collection called "shoppers"
        self.collection = self.database[collection_name]

        print("{} rows in data frame".format(len(data_frame.index)))

        # create ID column for use in MongoDB
        data_frame["_id"] = data_frame["ShopperId"]

        # convert to datetime for MongoDB
        data_frame["Date"] = pandas.to_datetime(data_frame["Date"])
        data_frame["TimeIn"] = pandas.to_datetime(data_frame["TimeIn"])

        # convert pandas data frame to dictionary
        data = data_frame.to_dict("records")

        # add data to the database
        self.collection.insert_many(data)

        # print number of rows in the database
        print("{} documents/rows in {} collection/table".format(
            self.collection.count_documents({}), self.collection.name))

    def query(self, query_dict):
        """
        Returns the results of a query.
        :param query_dict: Takes in a dictionary.
        :return: resulting query object.
        """
        pass

    def get_database_collection(self):
        """
        Returns the connections to the MongoDB database and collection as a tuple.
        :return: the connections to the MongoDB database and collection as a tuple.
        SystemError: If populate_shopper_database was not executed prior to running this method.
        """
        if self.database is None:
            raise SystemError("Please execute populate_shopper_database first, then try again.")
        return self.database, self.collection
