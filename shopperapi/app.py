"""Shopper API for accessing shopper data in MongoDB."""

from datetime import datetime
from dateutil import parser
from flask import Flask, request
from flask_restx import Api, Resource, fields
from bson import ObjectId

from shoppermodel import ShopperDatabase, ShopperTable
from configuration import HolidayModifiers, Rush, SeniorDiscount
from configuration import StoreModel, DayModifiers, TimeFrame

APP = Flask(__name__)
API = Api(APP, title='Shopper API', description='Access generated mock shopper data')

DB = ShopperDatabase()
DB.connect_to_client()


default_parameters = {
    "name": "default",
    "start_date" : '2020-01-01',
	"end_date" : '2020-3-31',
	"open_time" : "06:00",
	"close_time" : "21:00",
	"daily_average_traffic" : {
		"Monday" : 800,
		"Tuesday" : 1000,
		"Wednesday" : 1200,
		"Thursday" : 900,
		"Friday" : 2500,
		"Saturday" : 4000,
		"Sunday" : 5000
	},
	"lunch_rush" : {
		"start_time" : "12:00",
		"end_time" : "13:00",
		"time_spent" : 10,
		"percent" : 0.1
	},
	"dinner_rush" : {
		"start_time" : "17:00",
		"end_time" : "18:30",
		"time_spent" : 10,
		"percent" : 0.15
	},
	"day_modifiers" : {
		"min_time_spent" : 6,
		"avg_time_spent" : 25,
		"max_time_spent" : 75,
		"weekend_time_spent" : 60,
		"sunny_traffic_percent" : 0.4,
		"sunny_chance_percent" : 0.3,
		"sunny_time_spent" : 15
	},
	"holiday_modifiers" : {
		"holiday_percent" : 0.2,
		"day_before_percent" : 0.4,
		"week_before_percent" : 0.15
	},
	"senior_discount" : {
		"start_time" : "10:00",
		"end_time" : "12:00",
		"min_time_spent" : 45,
		"max_time_spent" : 60,
		"percent" : 0.2,
		"day" : "Tuesday"
	}
}

def generate_config(parameter_set):
    """
    Takes parameter dictionary and creates configuration objects used to generate shopper data
    :param parameter_set: dictionary of parameters and their corresponding values {parameter: value}
    :return: configuration objects initialized with data from parameters dictionary
    """

    time_frame = TimeFrame(parameter_set["start_date"], parameter_set["end_date"])

    lunch_rush = Rush(parameter_set["lunch_rush"]["start_time"], parameter_set["lunch_rush"]["end_time"], 
                      parameter_set["lunch_rush"]["time_spent"], parameter_set["lunch_rush"]["percent"])
    dinner_rush = Rush(parameter_set["dinner_rush"]["start_time"], parameter_set["dinner_rush"]["end_time"],
                       parameter_set["dinner_rush"]["time_spent"], parameter_set["dinner_rush"]["percent"])

    senior_discount = SeniorDiscount(parameter_set["senior_discount"]["start_time"], 
                                     parameter_set["senior_discount"]["end_time"], 
                                     parameter_set["senior_discount"]["min_time_spent"],
                                     parameter_set["senior_discount"]["max_time_spent"], 
                                     parameter_set["senior_discount"]["percent"])

    holiday_modifiers = HolidayModifiers(parameter_set["holiday_modifiers"]["holiday_percent"], 
                                         parameter_set["holiday_modifiers"]["day_before_percent"],
                                         parameter_set["holiday_modifiers"]["week_before_percent"])

    day_modifiers = DayModifiers(parameter_set["day_modifiers"]["min_time_spent"], 
                                 parameter_set["day_modifiers"]["avg_time_spent"], 
                                 parameter_set["day_modifiers"]["max_time_spent"],
                                 parameter_set["day_modifiers"]["weekend_time_spent"], 
                                 parameter_set["day_modifiers"]["sunny_traffic_percent"],
                                 parameter_set["day_modifiers"]["sunny_chance_percent"], 
                                 parameter_set["day_modifiers"]["sunny_time_spent"])

    avg_shopper_traffic = parameter_set["daily_average_traffic"]

    store_model = StoreModel(lunch_rush, dinner_rush, holiday_modifiers, day_modifiers,
                             senior_discount, avg_shopper_traffic, parameter_set["open_time"],
                             parameter_set["close_time"], parameter_set["senior_discount"]["percent"])

    return store_model, time_frame


def get_config_from_db(parameter_set_name):
    """
    Takes parameter name in MongoDB and creates configuration objects used to generate shopper data
    :param parameter_set_name: name of the parameter set stored in MongoDB
    :return: configuration objects initialized with data from parameters dictionary
    """

    query_dict = {"name": parameter_set_name}

    parameter_set = DB.query(query_dict=query_dict, collection_name="parameters")

    return generate_config(parameter_set)


def generate_shoppers(parameter_set_name):
    """
    Generates shopper data based on parameter set with given name in db, saves to the database
    :param parameter_set_name: name of parameter set in the database
    :return: None
    """
    store_model, time_frame = get_config_from_db(parameter_set_name)
    shopper_table = ShopperTable(store_model, time_frame)
    shopper_table.create_table()

    # create database class and connect to the database and populate
    database = ShopperDatabase()
    database.connect_to_client()
    database.populate_shopper_database(shopper_table, "default")


# If parameters collection doesn't exist, add default parameter set
database = DB.get_database()
if "parameters" not in database.list_collection_names():
    # add default parameter
    DB.update_document({"name": "default"}, default_parameters, collection_name="parameters")

# If shoppers collection doesn't exist, generate shoppers
if "shoppers" not in database.list_collection_names():
    # generate shoppers
    generate_shoppers("default")


def boolean(text):
    """
    Returns boolean for the provided text. Ignores lower/upper case of the text.
    :param text: string version of boolean (true, t, false, t).
    :return the given text as a boolean or an error message.
    """
    if text is None:
        return None

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