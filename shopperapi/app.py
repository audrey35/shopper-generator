from datetime import datetime
from calendar import day_name
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
from shoppermodel import ShopperDatabase


app = Flask(__name__)

db = ShopperDatabase()


def boolean(text):
    text = str(text)
    if text.lower() in ["true", "t"]:
        return True
    if text.lower() in ["false", "f"]:
        return False
    raise ValueError("Value must be true/false.")


def query_output_formatter(collections, query_dict, result_dict):
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
    return "Welcome to the Shopper API!"


url = "/<string:db_name>/<string:collection_name>/<int:shopper_id>/<string:date>/<string:day_of_week>/"
url += "<string:time_in>/<int:time_spent>/<string:is_senior>/<string:is_sunny>"


@app.route(url, methods=["POST"])
def shopper(db_name, collection_name, shopper_id, date, day_of_week, time_in, time_spent, is_senior, is_sunny):
    try:
        db.connect_to_client(database_name=db_name)
    except(ConnectionError):
        pass
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except:
        return "Invalid Date " + date
    if day_of_week not in day_name:
        return "Invalid Day Of Week " + day_of_week
    try:
        time_in = datetime.strptime(time_in, "%Y-%m-%d-%H-%M")
    except:
        return "Invalid time in " + str(time_in)
    try:
        is_senior = boolean(is_senior)
    except:
        return "Invalid senior " + str(is_senior)
    try:
        is_sunny = boolean(is_sunny)
    except:
        return "invalid sunny " + str(is_sunny)
    shopper_dict = {"_id": shopper_id, "Date": date, "DayOfWeek": day_of_week, "TimeIn": time_in, "TimeSpent": time_spent,
                    "IsSenior": is_senior, "IsSunny": is_sunny}
    db.add_document(shopper_dict, collection_name=collection_name)
    return "Successfully added a shopper to " + collection_name + " collection in " + db_name + " database."


@app.route("/list_db")
def list_db():
    client = MongoClient("mongodb://localhost:27017/")
    result = {}
    for db_name in client.list_database_names():
        result[db_name] = []
        for col_name in client[db_name].list_collection_names():
            result[db_name].append(col_name)
    return result


@app.route("/get_shoppers/<string:db_name>/<string:collection_name>")
def get_shoppers(db_name, collection_name):
    db.connect_to_client(database_name=db_name)
    result = {"database": db_name,
              "collection": collection_name,
              "documents": list(db.query(query_dict={}, collection_name=collection_name))}
    return result


@app.route("/get_shoppers/<string:db_name>/<string:start_date>/<string:end_date>")
def get_dates(db_name, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if abs(end.month - start.month) > 3:
        return jsonify(message="The range of dates should be within 3 months."), 404
    db.connect_to_client(database_name=db_name)
    database = db.get_database()
    collections = database.list_collection_names()
    query_dict = {"Date": {"$gte": start, "$lte": end}}
    result = {"start_date": start.strftime("%Y-%m-%d"),
              "end_date": end.strftime("%Y-%m-%d"),
              "database": db_name,
              "collections": {}
              }
    result = query_output_formatter(collections, query_dict, result)
    return result


@app.route("/get_shoppers/<string:db_name>/<string:is_senior>/<string:start_date>/<string:end_date>")
def get_senior_dates(db_name, is_senior, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if abs(end.month - start.month) > 3:
        return jsonify(message="The range of dates should be within 3 months."), 404
    db.connect_to_client(database_name=db_name)
    database = db.get_database()
    collections = database.list_collection_names()
    is_senior = boolean(is_senior)
    query_dict = {"Date": {"$gte": start, "$lte": end}, "IsSenior": is_senior}
    result = {"start_date": start.strftime("%Y-%m-%d"),
              "end_date": end.strftime("%Y-%m-%d"),
              "is_senior": is_senior,
              "database": db_name,
              "collections": {}
              }
    result = query_output_formatter(collections, query_dict, result)
    return result


@app.route("/sunny_weekend/<string:db_name>/<string:is_sunny>/<string:is_weekend>/<string:start_date>/<string:end_date>")
def get_sunny_weekend(db_name, is_sunny, is_weekend, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if abs(end.month - start.month) > 3:
        return jsonify(message="The range of dates should be within 3 months."), 404
    db.connect_to_client(database_name=db_name)
    database = db.get_database()
    collections = database.list_collection_names()
    is_sunny = boolean(is_sunny)
    is_weekend = boolean(is_weekend)
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
    result = query_output_formatter(collections, query_dict, result)
    return result


if __name__ == '__main__':
    app.run()
