"""Represents the MongoDB database for the shopper data."""
from datetime import datetime

import pandas
import pymongo
from bson import ObjectId
from os import environ


class ShopperDatabase:
    """
    Represents the MongoDB database for the shopper data.
    """

    def __init__(self):
        """
        Instantiates the ShopperDatabase object.
        """
        self.uri = environ.get('MONGODB_URI')
        self.database_name = "shoppers_db"
        self.client = None
        self.database = None
        self.collections = {}

    def connect_to_client(self):
        """
        Connects to the MongoDB client and database.
        :param uri: URI for the MongoDB.
        :param database_name: name of the MongoDB database to connect to.
        """
        if self.client is None:
            self.database_name = database_name
            self.client = pymongo.MongoClient(uri)
            # Connect to a database (MongoDB will create, if it doesn't exist)
            self.database = self.client[database_name]

    def close_client(self):
        """Closes the connection to the MongoDB client."""
        if self.client is not None:
            self.client = self.client.close()
            del self.database
            del self.collections
        else:
            raise ConnectionError('No client connection established.')

    def populate_shopper_database(self, shopper_table, parameter_set_name, collection_name="shoppers"):
        """
        Populates the shopper database with the given pandas data frame
        by converting the data frame into a records-based dictionary and
        inserting it into a MongoDB database collection. If the collection exists,
        then the program will replace the existing collection and associated
        parameters with the new data provided.
        :param shopper_table: the object that contains the data to be added into
        the database.
        :param collection_name: a unique name for the collection to be created.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        """
        if self.client is None and self.uri != "" and self.database_name != "":
            self.connect_to_client(self.uri, self.database_name)
        elif self.client is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")

        data_frame = shopper_table.data_frame

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

        # insert parameter id
        data_frame.insert(len(data_frame.columns), "parameter_name",
                          [parameter_set_name for i in range(0, len(data_frame))])

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

    def update_document(self, unique_value, shopper_dict, collection_name="shoppers"):
        """
        Updates a document in the MongoDB database, adds a document if not found.
        :param unique_value: a value that uniquely identifies the record {"field_name": value}
        :param shopper_dict: document details as a dictionary.
        :param collection_name: name of the collection.
        """
        if self.client is None and self.uri != "" and self.database_name != "":
            self.connect_to_client(self.uri, self.database_name)
        elif self.client is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")

        # Create/Connect to a collection
        collection = self.database[collection_name]

        result = collection.update_one(unique_value, {"$set": shopper_dict}, upsert=True)

        if (result.modified_count == 1) and (result.upserted_id == None):
            return {"result": 1, "message": "Successfully updated the document."}
        
        elif (result.modified_count == 0) and (result.upserted_id != None):
            return {"result": 2, "message": "Successfully added the document."}

        else:
            return {"result": 0, "message": "Could not update/add the document."}

    def db_query(self, query_dict, result_dict, limit=0):
        """
        Returns the dictionary output to be returned by the API
        for a query.
        :param query_dict: query result from the MongoDB.
        :param result_dict: query result formatted as a dictionary.
        :param limit: the amount of document to return in a query, default 0 means no limit
        :return: formatted dictionary of the query result.
        """
        collections = self.database.list_collection_names()
        for col in collections:
            if col == "parameters":
                continue
            query = self.query(query_dict=query_dict, collection_name=col, limit=limit)
            if query != {}:
                result_dict["collections"][col] = query
        return result_dict

    def query(self, query_dict: dict, sort_list=None, collection_name="shoppers"):
        """
        Returns the results of a query.
        :param query_dict: a dictionary of the query statement.
        :param sort_list: a list of fields to sort by (optional).
        :param collection_name: name of the collection to query on.
        :param limit: the amount of document to return in a query, default 0 means no limit
        :return: resulting query object.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        ValueError: If collection does not exist in the database.
        """
        collection = self.__verify_connections(collection_name)

        if not isinstance(sort_list, list) or sort_list is None:
            output = collection.find(query_dict)
        else:
            output = collection.find(query_dict).sort(sort_list)

        count = collection.count_documents(query_dict)

        if count == 0:
            return {}

        result = []
        for document in output:
            # document data type: dictionary
            for key in document:
                value = document[key]
                # ObjectId and datetime values converted to string
                if isinstance(value, (ObjectId, datetime)):
                    document[key] = str(document[key])
            if count == 1:
                return document
            result.append(document)

        return result

    def find_parameters(self):
        """
        Collect the list of parameters that were included in the shopper database
        :return: a list of the parameters, each parameter is a dictionary
        """
        collection = self.__verify_connections("parameters")
        param_list = collection.find()
        results = []
        for document in param_list:
            results.append(str(document['_id']))

        return results

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

    def get_database(self):
        """
        Returns the connections to the MongoDB database.
        :return: the connections to the MongoDB database.
        ConnectionError: If populate_shopper_database was not executed prior to running this method.
        """
        if self.database is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")
        return self.database

    def delete_collection(self, collection_name):
        """
        Deletes a collection and its associated parameter set
        from the MongoDB database.
        :param collection_name: name of the collection to delete.
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
            # get the first document in the collection
            param_id_dict = self.database[collection_name].find_one()
            # get the parameter_id value
            param_id = param_id_dict["parameter_id"]
            # delete the parameter document with id from above
            self.database["parameters"].delete_one({"_id": param_id})
            # delete the collection
            self.database[collection_name].drop()

    def upload_parameters(self, store_model, time_frame):
        """
        Takes the parameters of that generated the data and uploads them to the database
        :param store_model: ShopperModel object
        :param time_frame: TimeFrame object
        :return: the id of the inserted result
        """
        if self.client is None and self.uri != "" and self.database_name != "":
            self.connect_to_client(self.uri, self.database_name)
        elif self.client is None:
            msg = "No database connection established. Please run connect_to_client "
            raise ConnectionError(msg + "before populating the database.")

        parameters = {
            "start_date": time_frame.start_date,
            "end_date": time_frame.end_date,
            "open_time": store_model.open_time.__str__(),
            "close_time": store_model.close_time.__str__(),
            "daily_average_traffic": store_model.avg_shopper_traffic,
            "lunch_rush": {
                "start_time": store_model.lunch_rush.start_time.__str__(),
                "end_time": store_model.lunch_rush.end_time.__str__(),
                "time_spent": store_model.lunch_rush.time_spent,
                "percent": store_model.lunch_rush.percent
            },
            "dinner_rush": {
                "start_time": store_model.dinner_rush.start_time.__str__(),
                "end_time": store_model.dinner_rush.end_time.__str__(),
                "time_spent": store_model.dinner_rush.time_spent,
                "percent": store_model.dinner_rush.percent
            },
            "day_modifiers": {
                "min_time_spent": store_model.day_modifiers.min_time_spent,
                "avg_time_spent": store_model.day_modifiers.avg_time_spent,
                "max_time_spent": store_model.day_modifiers.max_time_spent,
                "weekend_time_spent": store_model.day_modifiers.weekend_time_spent,
                "sunny_traffic_percent": store_model.day_modifiers.sunny_traffic_percent,
                "sunny_chance_percent": store_model.day_modifiers.sunny_chance_percent,
                "sunny_time_spent": store_model.day_modifiers.sunny_time_spent
            },
            "holiday_modifiers": {
                "holiday_percent": store_model.holiday_modifiers.holiday_percent,
                "day_before_percent": store_model.holiday_modifiers.day_before_percent,
                "week_before_percent": store_model.holiday_modifiers.week_before_percent
            },
            "senior_discount": {
                "start_time": store_model.senior_discount.start_time.__str__(),
                "end_time": store_model.senior_discount.end_time.__str__(),
                "min_time_spent": store_model.senior_discount.min_time_spent,
                "max_time_spent": store_model.senior_discount.max_time_spent,
                "percent": store_model.senior_discount.percent,
                "day": store_model.senior_discount.day_name
            }
        }

        collection = self.database["parameters"]
        result = collection.insert_one(parameters)
        return result.inserted_id

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
