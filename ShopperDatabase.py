import pymongo

class ShopperDatabase(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.database = None
        self.collection = None

    def populate_shopper_database(self, data_frame):
        """
        Populates the shopper database with the given pandas data frame.
        :param data_frame: pandas data frame containing the data to pull
        into the MongoDB database. The name of the database and collection
        comes from the configuration class (parameters are edited in command line).
        :return: Nothing.
        """
        

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
        if self.database == None:
            raise SystemError("Please execute populate_shopper_database first, then try again.")
        return self.database, self.collection