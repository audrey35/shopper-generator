"""Shopper API for accessing shopper data in MongoDB."""

from datetime import datetime
from calendar import day_name
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
from shoppermodel import ShopperDatabase

app = Flask(__name__)

db = ShopperDatabase()


def boolean(text):
    """
    Returns boolean for the provided text. Ignores lower/upper case of the text.
    :param text: string version of boolean (true, t, false, t).
    :return the given text as a boolean or an error message.
    """
    text = str(text)
    if text.lower() in ["true", "t"]:
        return True
    if text.lower() in ["false", "f"]:
        return False
    return "Value must be true/false."


def check_dates(start_date, end_date):
    """
    Returns the start and end dates as datetime or
    a message if the dates are invalid.
    :param start_date: start date as a string (ex. 2018-2-10).
    :param end_date: end date as a string (ex. 2018-3-5).
    :return: a tuple of start and end dates as datetime or
    a tuple of error messages.
    """
    message = ""
    start = ""
    end = ""

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        message += "Invalid Date {}. ".format(start_date)

    try:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        message += "Invalid Date {}. ".format(end_date)

    if message != "":
        return message, message

    if abs(end.month - start.month) > 3:
        message += "The range of dates should be within 3 months."

    if message != "":
        return message, message
    return start, end


def query_output_formatter(collections, query_dict, result_dict):
    """
    Returns the dictionary output to be returned by the API
    for a query.
    :param collections: list of collection names.
    :param query_dict: query result from the MongoDB.
    :param result_dict: query result formatted as a dictionary.
    :return: formatted dictionary of the query result.
    """
    for col in collections:
        if col == "parameters":
            continue
        query = db.query(query_dict=query_dict, collection_name=col)
        keys = query[0].keys()
        output = {}
        result_dict["collections"][col] = []
        for document in query:
            for k in keys:
                output[k] = str(document[k])
                if isinstance(document[k], ObjectId):
                    output[k] = str(document[k])
            result_dict["collections"][col].append(output)
    return result_dict


@app.route("/")
def home():
    """
    Home page of the API.
    :return: a welcome message.
    """
    return jsonify(message="Welcome to the Shopper API!")


URL = "/add-shopper/<string:db_name>/<string:collection_name>/<int:shopper_id>/"
URL += "<string:date>/<string:day_of_week>/"
URL += "<string:time_in>/<int:time_spent>/<string:is_senior>/<string:is_sunny>"


@app.route(URL, methods=["POST"])
def shopper(db_name, collection_name, shopper_id, date, day_of_week,
            time_in, time_spent, is_senior, is_sunny):
    """
    Adds a document to the specified MongoDB database collection
    with provided information.
    :param db_name: name of the MongoDB database.
    :param collection_name: name of the MongoDB collection.
    :param shopper_id: unique id for the shopper as an integer.
    :param date: date the shopper visited as a string (ex. 2018-03-05).
    :param day_of_week: day of week the shopper visited (ex. Monday).
    :param time_in: time that the shopper entered the store (ex. 13:35).
    :param time_spent: amount of time shopper spent in minutes.
    :param is_senior: true if shopper is a senior else false.
    :param is_sunny: true if the day is sunny else false.
    :return: a message indicating whether the post operation was successful.
    """
    try:
        db.connect_to_client(database_name=db_name)
    except ConnectionError:
        return jsonify(message="Invalid database name " + db_name), 404

    message = ""
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        message += "Invalid Date {}. ".format(date)

    if day_of_week not in day_name:
        message += "Invalid Day Of Week {}. ".format(day_of_week)

    try:
        time_in = datetime.strptime(time_in, "%Y-%m-%d-%H-%M")
    except ValueError:
        message += "Invalid time in {}. ".format(time_in)

    try:
        is_senior = boolean(is_senior)
    except ValueError:
        message += "Invalid senior {}. ".format(is_senior)

    try:
        is_sunny = boolean(is_sunny)
    except ValueError:
        message += "Invalid sunny {}. ".format(is_sunny)

    if message != "":
        return jsonify(message=message), 404

    shopper_dict = {"_id": shopper_id, "Date": date, "DayOfWeek": day_of_week,
                    "TimeIn": time_in, "TimeSpent": time_spent,
                    "IsSenior": is_senior, "IsSunny": is_sunny}
    try:
        db.add_document(shopper_dict, collection_name=collection_name)
    except:
        return jsonify("Could not add the shopper details to the database collection."), 404

    msg = "Successfully added a shopper to " + collection_name
    msg += " collection in " + db_name + " database."
    return jsonify(message=msg)


@app.route('/list-databases')
def list_db():
    """
    Returns a dictionary of the available MongoDB databases and
    name of collections in each database.
    """
    client = MongoClient("mongodb://localhost:27017/")
    result = {}
    for db_name in client.list_database_names():
        result[db_name] = []
        for col_name in client[db_name].list_collection_names():
            result[db_name].append(col_name)
    return result


@app.route("/get-shoppers/<string:db_name>/<string:collection_name>")
def get_shoppers(db_name, collection_name):
    """
    Returns a dictionary of all documents in the MongoDB database collection.
    :param db_name: name of the MongoDB database.
    :param collection_name: name of the collection in the database.
    :return: a dictionary of all documents in the MongoDB database collection.
    """
    try:
        db.connect_to_client(database_name=db_name)
    except ConnectionError:
        return jsonify(message="Invalid database name " + db_name), 404

    result = {"database": db_name,
              "collection": collection_name,
              "documents": list(db.query(query_dict={}, collection_name=collection_name))}

    return result


@app.route("/get-shoppers/<string:db_name>/<string:start_date>/<string:end_date>")
def get_dates(db_name, start_date, end_date):
    """
    Return a dictionary of the documents in the database with dates
    in range of given start and end dates. The start and end dates must be within
    3 months.
    :param db_name: name of the MongoDB database.
    :param start_date: start date for the range of dates to select (ex. 2018-03-05).
    :param end_date: end date for the range of dates to select (ex. 2018-04-10).
    :return: Return a dictionary of the documents in the database with dates
    in range of given start and end dates.
    """
    # check if start and end dates are valid.
    start, end = check_dates(start_date, end_date)
    if isinstance(start, str):
        return jsonify(start), 404

    # check if database connection is successful.
    try:
        db.connect_to_client(database_name=db_name)
    except ConnectionError:
        return jsonify(message="Invalid database name " + db_name), 404

    # prepare to run query on every collection in the database.
    database = db.get_database()
    collections = database.list_collection_names()
    query_dict = {"Date": {"$gte": start, "$lte": end}}
    result = {"start_date": start.strftime("%Y-%m-%d"),
              "end_date": end.strftime("%Y-%m-%d"),
              "database": db_name,
              "collections": {}
              }

    # run the query and format the output, then return the result.
    result = query_output_formatter(collections, query_dict, result)
    return result


URL = "/get-senior-shoppers/<string:db_name>/<string:is_senior>/"
URL += "<string:start_date>/<string:end_date>"


@app.route(URL)
def get_senior_dates(db_name, is_senior, start_date, end_date):
    """
    Return a dictionary of documents in the database that are within
    the range of the provided start and end dates and is senior is set
    to true. The start and end dates must be within 3 months.
    :param db_name: name of the MongoDB database.
    :param is_senior: true if selecting senior shoppers, false otherwise.
    :param start_date: start date for the range of dates to select (ex. 2018-03-05).
    :param end_date: end date for the range of dates to select (ex. 2018-04-10).
    :return: Return a dictionary of documents in the database that are within
    the range of the provided start and end dates and is senior is set
    to true.
    """
    # check if start and end dates are valid.
    start, end = check_dates(start_date, end_date)
    if isinstance(start, str):
        return jsonify(start), 404

    # check is_senior is a boolean value.
    is_senior = boolean(is_senior)
    if isinstance(is_senior, str):
        return jsonify(message=is_senior), 404

    # check if database connection is successful.
    try:
        db.connect_to_client(database_name=db_name)
    except ConnectionError:
        return jsonify(message="Invalid database name " + db_name), 404

    # prepare to run query on every collection in the database.
    database = db.get_database()
    collections = database.list_collection_names()
    query_dict = {"Date": {"$gte": start, "$lte": end}, "IsSenior": is_senior}
    result = {"start_date": start.strftime("%Y-%m-%d"),
              "end_date": end.strftime("%Y-%m-%d"),
              "is_senior": is_senior,
              "database": db_name,
              "collections": {}
              }

    # run the query and format the output, then return the result.
    result = query_output_formatter(collections, query_dict, result)
    return result


URL = "/get-sunny-weekend-shoppers/<string:db_name>/<string:is_sunny>/"
URL += "<string:is_weekend>/<string:start_date>/<string:end_date>"


@app.route(URL)
def get_sunny_weekend(db_name, is_sunny, is_weekend, start_date, end_date):
    """
    Return a dictionary of selected documents in the database. The documents
    are within the range of the provided start and end dates and the the shopper
    visited the store on a sunny or not sunny weekend or weekday.
    :param db_name: name of the database.
    :param is_sunny: true if selecting sunny days, false otherwise.
    :param is_weekend: true if selecting weekends, false otherwise.
    :param start_date: start date for the range of dates to select (ex. 2018-03-05).
    :param end_date: end date for the range of dates to select (ex. 2018-04-10).
    :return: Return a dictionary of selected documents in the database. The documents
    are within the range of the provided start and end dates and the the shopper
    visited the store on a sunny or not sunny weekend or weekday.
    """
    # check if start and end dates are valid.
    start, end = check_dates(start_date, end_date)
    if isinstance(start, str):
        return jsonify(start), 404

    # check if is_sunny is boolean.
    is_sunny = boolean(is_sunny)
    if isinstance(is_sunny, str):
        return jsonify(message=is_sunny), 404

    # check if is_weekend is boolean.
    is_weekend = boolean(is_weekend)
    if isinstance(is_weekend, str):
        return jsonify(message=is_weekend), 404

    # connect to the database.
    try:
        db.connect_to_client(database_name=db_name)
    except ConnectionError:
        return jsonify(message="Invalid database name " + db_name), 404

    # prepare to run query on every collection in the database.
    database = db.get_database()
    collections = database.list_collection_names()
    if is_weekend:
        query_dict = {"Date": {"$gte": start, "$lte": end},
                      "$or": [{"DayOfWeek": "Saturday"}, {"DayOfWeek": "Sunday"}],
                      "IsSunny": is_sunny,
                      }
        result = {"start_date": start.strftime("%Y-%m-%d"),
                  "end_date": end.strftime("%Y-%m-%d"),
                  "DayOfWeek": ["Saturday, Sunday"],
                  "IsSunny": is_sunny,
                  "database": db_name,
                  "collections": {}
                  }
    else:
        query_dict = {"Date": {"$gte": start, "$lte": end},
                      "$or": [{"DayOfWeek": "Monday"}, {"DayOfWeek": "Tuesday"},
                              {"DayOfWeek": "Wednesday"},
                              {"DayOfWeek": "Thursday"}, {"DayOfWeek": "Friday"}],
                      "IsSunny": is_sunny}
        result = {"start_date": start.strftime("%Y-%m-%d"),
                  "end_date": end.strftime("%Y-%m-%d"),
                  "DayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                  "IsSunny": is_sunny,
                  "database": db_name,
                  "collections": {}
                  }

    # run the query and format the output, then return the result.
    result = query_output_formatter(collections, query_dict, result)
    return result


if __name__ == '__main__':
    app.run()
