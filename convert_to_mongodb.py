"""
Research on converting CSV to Mongo DB
"""

from datetime import datetime as dt
import json
import pymongo
import pandas

# Create a MongoClient Object and specify a connection URL
my_client = pymongo.MongoClient("mongodb://localhost:27017/")

# Deletes the MongoDB database "shoppers_db"
# my_client.drop_database("shoppers_db")

# Connect to a database (MongoDB will create, if it doesn't exist)
my_db = my_client["shoppers_db"]

# Delete "shoppers" collection if it exists
col_list = my_db.list_collection_names()
if "shoppers" in col_list:
    my_db["shoppers"].drop()

# Create a collection called "shoppers"
my_col = my_db["shoppers"]


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


# print name of database
print(my_db.name)

start = dt.now()

#### Choose one of the methods to run. Comment out the other.
# csv_to_mongodb(my_col)
csv_to_json_to_mongodb(my_col)

print(my_col.count_documents({}))
print("Time taken to add csv to MongoDB: {}".format(dt.now() - start))
