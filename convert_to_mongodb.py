"""
Research on converting CSV to Mongo DB
"""

from datetime import datetime as dt
import json
import pymongo
import pandas


def set_up_mongodb(database_name="shoppers_db", collection_name="shoppers"):
    """
    Set up the MongoDB connection and returns the connection.
    The MongoDB database or collection will be created if it doesn't exist.
    Requires pymongo to run.
    :param database_name: name of the MongoDB database.
    :param collection_name: name of the collection/table inside the database.
    :return: MongoDB database connection and collection connection objects as a tuple.
    """
    # Create a MongoClient Object and specify a connection URL
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Deletes the MongoDB database "shoppers_db"
    # my_client.drop_database("shoppers_db")

    # Connect to a database (MongoDB will create, if it doesn't exist)
    database = client[database_name]

    # Delete "shoppers" collection if it exists (allows reruns)
    col_list = database.list_collection_names()
    if collection_name in col_list:
        database[collection_name].drop()

    # Create a collection called "shoppers"
    collection = database[collection_name]

    return database, collection


def csv_to_mongodb(mongo_db_collection, csv_path="shoppers.csv"):
    """
    Adds CSV data to a MongoDB collection by using pandas to convert
    the csv to a records-based dictionary (different format than the
    dictionary used to create a data frame).
    :param mongo_db_collection: connection object for a MongoDB collection
    :param csv_path: path to the data to be added as a csv
    :return: mongo_db_collection
    """
    # Load the csv file into a pandas data frame.
    data = pandas.read_csv(csv_path, encoding="ISO-8859-1")
    print("{} rows in data frame".format(len(data.index)))

    # create ID column for use in MongoDB
    data["_id"] = data["ShopperId"]

    # convert to datetime for MongoDB
    data["Date"] = pandas.to_datetime(data["Date"])
    data["TimeIn"] = pandas.to_datetime(data["TimeIn"])
    # convert pandas data frame to dictionary
    data = data.to_dict("records")

    # add data to the database
    mongo_db_collection.insert_many(data)

    # print number of rows in the database
    print("{} documents/rows in {} collection/table".format(
        mongo_db_collection.count_documents({}), mongo_db_collection.name))

    return mongo_db_collection


def csv_to_json_to_mongodb(mongo_db_collection, csv_path="shoppers.csv"):
    """
        Adds CSV data to a MongoDB collection by using pandas to convert the
        csv to a records-based json format.
        :param mongo_db_collection: connection object for a MongoDB collection
        :param csv_path: path to the data to be added as a csv
        :return: mongo_db_collection
        """
    # Load the csv file into a pandas data frame.
    data = pandas.read_csv(csv_path, encoding="ISO-8859-1")
    print("{} rows in data frame".format(len(data.index)))

    # convert pandas data frame to json
    data = data.to_json(orient="records")

    # load json
    records = json.loads(data)

    # add data to the database
    mongo_db_collection.insert_many(records)

    # print number of rows in the database
    print("{} documents/rows in {} collection/table".format(
        mongo_db_collection.count_documents({}), mongo_db_collection.name))

    return mongo_db_collection


def main():
    """
    only runs if this is the main file.
    """
    if __name__ == "__main__":
        my_db, my_col = set_up_mongodb()

        # print name of database
        print(my_db.name)

        start = dt.now()

        # ***Choose one of the methods to run. Comment out the other.***
        # csv_to_mongodb(my_col)
        csv_to_json_to_mongodb(my_col)

        print(my_col.count_documents({}))
        print("Time taken to add csv to MongoDB: {}".format(dt.now() - start))


main()
