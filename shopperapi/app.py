"""Shopper API for accessing shopper data in MongoDB."""

from datetime import datetime
from this import d
from dateutil import parser
from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
from bson import ObjectId
from pymongo import ASCENDING

from shoppermodel import ShopperDatabase, ShopperTable
from configuration import HolidayModifiers, Rush, SeniorDiscount
from configuration import StoreModel, DayModifiers, TimeFrame

APP = Flask(__name__)
API = Api(APP, title='Shopper API', description='Access generated mock shopper data', doc='/doc/')

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

    parameter_set = parameter_set["documents"][0]

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

    if parameter_set["count"] == 0:
        return 0, 0

    return generate_config(parameter_set)


def generate_shoppers(parameter_set_name):
    """
    Generates shopper data based on parameter set with given name in db, saves to the database
    :param parameter_set_name: name of parameter set in the database
    :return: None
    """
    store_model, time_frame = get_config_from_db(parameter_set_name)

    if type(store_model) == int:
        message = "Could not generate shoppers because parameters named "
        message += parameter_set_name + " doesn't exist."
        return {"result": 0, "message": message}

    shopper_table = ShopperTable(store_model, time_frame)
    shopper_table.create_table()

    # create database class and connect to the database and populate
    database = ShopperDatabase()
    database.connect_to_client()
    database.populate_shopper_database(shopper_table, parameter_set_name)

    message = "Successfully generated shoppers using "
    message += parameter_set_name + " parameters."

    return {"result": 1, "message": message}


# GENERATE DEFAULT PARAMETERS AND DATA IF MISSING

# If parameters collection doesn't exist, add default parameter set
database = DB.get_database()
if "parameters" not in database.list_collection_names():
    # add default parameter
    DB.update_document({"name": "default"}, default_parameters, collection_name="parameters")

# If shoppers collection doesn't exist, generate shoppers
if "default" not in database.list_collection_names():
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


# API: GET ALL PARAMETERS

"""
Implemented Flask-RestPLUS and Swagger UI by referring to
https://morioh.com/p/7c1ce2462a74
"""

GET_STATUS = "Could not retrieve information"

NAME_SPACE = API.namespace('parameters', description='Parameters used to '
                                                     'generate the mock shopper data')

parser = reqparse.RequestParser()

parser.add_argument('name', type=str, help='Name of the parameter set being added', 
                    required=True)

# Start and End Dates
parser.add_argument('start-date', default='2020-01-01', type=str,
                    help='The starting date to generate data for in format: 2019-01-01', 
                    required=True)
parser.add_argument('end-date', default='2020-3-31', type=str,
                    help='The ending date to generate data for in format: 2020-12-31', 
                    required=True)

# Open and Close Time
parser.add_argument('open-time', default='06:00', type=str,
                    help='The opening time of the store: 06:00', 
                    required=True)
parser.add_argument('close-time', default='21:00', type=str,
                    help='The closing time of the store: 21:00', 
                    required=True)

# Average Traffic per Day
parser.add_argument('mon-traffic', default=800, type=int,
                    help='Average number of shoppers on Monday: 800', 
                    required=True)
parser.add_argument('tue-traffic', default=1000, type=int,
                    help='Average number of shoppers on Tuesday: 1000', 
                    required=True)
parser.add_argument('wed-traffic', default=1200, type=int,
                    help='Average number of shoppers on Wednesday: 1200', 
                    required=True)
parser.add_argument('thu-traffic', default=900, type=int,
                    help='Average number of shoppers on Thursday: 900', 
                    required=True)
parser.add_argument('fri-traffic', default=2500, type=int,
                    help='Average number of shoppers on Friday: 2500', 
                    required=True)
parser.add_argument('sat-traffic', default=4000, type=int,
                    help='Average number of shoppers on Saturday: 4000', 
                    required=True)
parser.add_argument('sun-traffic', default=5000, type=int,
                    help='Average number of shoppers on Sunday: 5000', 
                    required=True)

# Lunch Rush
parser.add_argument('lunch-start', default='12:00', type=str,
                    help='The time the lunch rush starts at in the store: 12:00', 
                    required=True)
parser.add_argument('lunch-end', default='13:00', type=str,
                    help='The time the lunch rush ends at in the store: 13:00', 
                    required=True)
parser.add_argument('lunch-time-spent', default=10, type=int,
                    help='Average amount of time shoppers are spending at lunch: 10', 
                    required=True)
parser.add_argument('lunch-percent', default=0.10, type=float,
                    help='Percent of shoppers coming into the store at lunchtime: 0.10', 
                    required=True)

# Dinner Rush
parser.add_argument('dinner-start', default='17:00', type=str,
                    help='The time the dinner rush starts at in the store: 12:00', 
                    required=True)
parser.add_argument('dinner-end', default='18:30', type=str,
                    help='The time the dinner rush ends at in the store: 13:00', 
                    required=True)
parser.add_argument('dinner-time-spent', default=10, type=int,
                    help='Average amount of time shoppers are spending at dinner: 20', 
                    required=True)
parser.add_argument('dinner-percent', default=0.15, type=float,
                    help='Percent of shoppers coming into the store at dinnertime: 0.15', 
                    required=True)

# Time Spent
parser.add_argument('min-time-spent', default=6, type=int,
                    help='Minimum number of minutes that shoppers spend in the store: 6', 
                    required=True)
parser.add_argument('avg-time-spent', default=25, type=int,
                    help='Average number of minutes that shoppers spend in the store: 25', 
                    required=True)
parser.add_argument('max-time-spent', default=75, type=int,
                    help='Maximum number of minutes that shoppers spend in the store: 75', 
                    required=True)

# Sunny Percentages
parser.add_argument('sunny-traffic-percent', default=0.4, type=float,
                    help='The percent increase in traffic during a sunny weekend', 
                    required=True)
parser.add_argument('sunny-chance-percent', default=0.3, type=float,
                    help='The percent chance that a weekend is sunny', 
                    required=True)
parser.add_argument('sunny-time-spent', default=15, type=int,
                    help='The time shoppers are spending on a sunny weekend', 
                    required=True)

# Weekend and Sunny
parser.add_argument('weekend-time-spent', default=60, type=int,
                    help='Average number of minutes that shoppers spend in the store on '
                            'weekends: 60', required=True)

# Holidays
parser.add_argument('holiday-percent', default=0.2, type=float,
                    help='The percent decrease of shoppers due to a holiday', 
                    required=True)
parser.add_argument('day-before-holiday-percent', default=0.4, type=float,
                    help='The percent increase of shoppers due the day before a holiday', 
                    required=True)
parser.add_argument('week-before-holiday-percent', default=0.15, type=float,
                    help='The percent increase of shoppers when day is within a week '
                            'before a holiday', 
                    required=True)

# Senior Discount
parser.add_argument('senior-start', default='10:00', type=str,
                    help='The time the senior discount starts at in the store: 10:00', 
                    required=True)
parser.add_argument('senior-end', default='12:00', type=str,
                    help='The time the senior discount end at in the store: 12:00', 
                    required=True)
parser.add_argument('senior-discount-percent', default=0.1, type=float,
                    help='Percent of seniors coming into the store on Tuesday from '
                            '10-12pm: 0.5', required=True)
parser.add_argument('senior-min-time-spent', default=45, type=int,
                    help='Minimum number of minutes that senior shoppers spend in the store '
                            'during senior discount hours: 45', required=True)
parser.add_argument('senior-max-time-spent', default=60, type=int,
                    help='Maximum number of minutes that senior shoppers spend in the store '
                            'during senior discount hours: 60', required=True)
parser.add_argument('senior-percent', default=0.2, type=float,
                    help='Percent of seniors coming into the store: 0.2', required=True)
parser.add_argument('senior-day', default="Tuesday", type=str,
                    help='Day of week senior discount occurs: Tuesday', required=True)


@NAME_SPACE.route("")
class Parameter(Resource):
    """Retrieve all parameters in the MongoDB database"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def get(self):
        """
        Returns a dictionary of all parameters in the MongoDB database
        """
        try:
            return DB.query({}, [("name", ASCENDING)], "parameters")

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @API.expect(parser)
    def post(self):
        """
        Add/Update a set of parameters in the MongoDB database.
        """
        try:
            result = {}
            d = request.args

            if d["name"].lower() == "parameters":
                message =  "Could not add/update the parameters. "
                message += "Please use a name other than 'parameters'."
                return {"result": 0, "message": message}
            
            result["name"] = d["name"]
            result["start_date"] = d["start-date"]
            result["end_date"] = d["end-date"]
            result["open_time"] = d["open-time"]
            result["close_time"] = d["close-time"]
            result["daily_average_traffic"] = {
                "Monday": int(d["mon-traffic"]),
                "Tuesday": int(d["tue-traffic"]),
                "Wednesday": int(d["wed-traffic"]),
                "Thursday": int(d["thu-traffic"]),
                "Friday": int(d["fri-traffic"]),
                "Saturday": int(d["sat-traffic"]),
                "Sunday": int(d["sun-traffic"])
            }
            result["lunch_rush"] = {
                "start_time" : d["lunch-start"],
                "end_time" : d["lunch-end"],
                "time_spent" : int(d["lunch-time-spent"]),
                "percent" : float(d["lunch-percent"])
            }
            result["dinner_rush"] = {
                    "start_time" : d["dinner-start"],
                    "end_time" : d["dinner-end"],
                    "time_spent" : int(d["dinner-time-spent"]),
                    "percent" : float(d["dinner-percent"])
            }
            result["day_modifiers"] = {
                "min_time_spent" : int(d["min-time-spent"]),
                "avg_time_spent" : int(d["avg-time-spent"]),
                "max_time_spent" : int(d["max-time-spent"]),
                "weekend_time_spent" : int(d["weekend-time-spent"]),
                "sunny_traffic_percent" : float(d["sunny-traffic-percent"]),
                "sunny_chance_percent" : float(d["sunny-chance-percent"]),
                "sunny_time_spent" : int(d["sunny-time-spent"])
            }
            result["holiday_modifiers"] = {
                "holiday_percent" : float(d["holiday-percent"]),
                "day_before_percent" : float(d["day-before-holiday-percent"]),
                "week_before_percent" : float(d["week-before-holiday-percent"])
            }
            result["senior_discount"] = {
                "start_time": d["senior-start"],
                "end_time" : d["senior-end"],
                "min_time_spent" : int(d["senior-min-time-spent"]),
                "max_time_spent" : int(d["senior-max-time-spent"]),
                "percent" : float(d["senior-percent"]),
                "day" : d["senior-day"]
            }
            
            

            return DB.update_document({"name": d["name"]}, result, collection_name="parameters")

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@NAME_SPACE.route('/<string:parameter_name>')
class ParameterItem(Resource):
    """A set of parameters"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'parameter_name': 'Parameter name used to retrieve the set of '
                                     'parameters used to generate the mock shopper data'
                     }
             )
    def get(self, parameter_name):
        """
        Returns a set of parameters given a parameter name.
        """

        try:
            query_dict = {"name": parameter_name}

            query_result = DB.query(query_dict=query_dict, collection_name="parameters")

            return query_result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")
    

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'parameter_name': 'Parameter name of the set of '
                                     'parameters used to generate the mock shopper data'
                     }
             )
    def delete(self, parameter_name):
        """
        Deletes a set of parameters given a parameter name.
        """

        try:
            return DB.delete_document({"name": parameter_name}, collection_name="parameters")

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


@NAME_SPACE.route("/<string:parameter_name>/shoppers")
class Shopper(Resource):
    """Generates shopper data using the given parameters"""


    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'parameter_name': 'Parameter name of the set of '
                                     'parameters used to generate the mock shopper data'
                     }
             )
    def get(self, parameter_name):
        """
        Returns 1st 10 shoppers generated using the given parameters.
        """
        try:
            # if parameter_name isn't parameters (would overwrite parameters collection)
            if parameter_name.lower() != "parameters":
                result = DB.query({}, None, parameter_name, 10)
                if result["count"] == 0:
                    message = "Cannot get shoppers because they haven't "
                    message += "been generated using " + parameter_name + " parameters."
                    return {"result": 0, "message": message}
                    
                return result

            else:
                return {"result": 0, "message": "Can not get shoppers using parameters named 'parameters'."}

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'parameter_name': 'Parameter name of the set of '
                                     'parameters used to generate the mock shopper data'
                     }
             )
    def post(self, parameter_name):
        """
        Generates shoppers using the given parameters.
        """
        try:
            # if parameter_name isn't parameters (would overwrite parameters collection)
            if parameter_name.lower() != "parameters":
                result = generate_shoppers(parameter_name)

                return result

            else:
                return {"result": 0, "message": "Can not generate shoppers using parameters named 'parameters'."}

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")