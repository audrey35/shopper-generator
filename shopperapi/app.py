from datetime import datetime
from calendar import day_name
from flask import Flask
from pymongo import MongoClient
from shoppermodel import ShopperDatabase





app = Flask(__name__)





@app.route("/")
def home():
    return "Welcome to the Shopper API!"


url = "/<string:db_name>/<string:collection_name>/<int:shopper_id>/<string:date>/<string:day_of_week>/"
url += "<string:time_in>/<int:time_spent>/<string:is_senior>/<string:is_sunny>"

def boolean(text):
    text = str(text)
    if text.lower() in ["true", "t"]:
        return True
    if text.lower() in ["false", "f"]:
        return False
    raise ValueError("Value must be true/false.")


db = ShopperDatabase()


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
    database, collection = db.get_database_collection(collection_name=collection_name)
    result = {"database": db_name,
              "collection": collection_name,
              "documents": list(collection.find())}
    return result


"""
Potential Query
@app.route("/get_shoppers/<string:db_name>/<string:start_date>/<string:end_date>")
returns a dictionary
{
    "start_date": "2018-01-03",
    "end_date": "2018-02-03",
    "database": "shoppers_db",
    "collections": {
        "shoppers": [shopper1_dict, shopper2_dict],
        "collection_2": [shopper1_dict, shopper2_dict]
    }
}
"""


if __name__ == '__main__':
    app.run()
