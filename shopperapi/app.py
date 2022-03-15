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
DB_NAME = "shoppers_db"
DB.connect_to_client(database_name=DB_NAME)


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


"""
Implemented Flask-RestPLUS and Swagger UI by referring to
https://morioh.com/p/7c1ce2462a74
"""

GET_STATUS = "Could not retrieve information"

NAME_SPACE = API.namespace('collections', description='Collections in the MongoDB database')


@NAME_SPACE.route("")
class Collection(Resource):
    """List of collections in the MongoDB database"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def get(self):
        """
        Returns a dictionary of all collections in the MongoDB database
        """
        try:
            result = {"collection_name": []}
            database = DB.get_database()
            result["database_name"] = DB_NAME
            for col_name in database.list_collection_names():
                result["collection_name"].append(col_name)
            return result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


NAME_SPACE = API.namespace('parameters', description='Parameters used to '
                                                     'generate the mock shopper data')


@NAME_SPACE.route("")
class Parameter(Resource):
    """List of parameters"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def get(self):
        """
        Returns a dictionary of all the parameter documents in the database
        """
        try:
            result = {"documents": DB.find_parameters()}

            return result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@NAME_SPACE.route('/<string:parameter_id>')
class ParameterItem(Resource):
    """A set of parameters"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'parameter_id': 'Parameter ID used to retrieve the set of '
                                     'parameters used to generate the mock shopper data'
                     }
             )
    def get(self, parameter_id):
        """
        Returns a set of parameters given a parameter ID.
        """

        try:
            query_dict = {"_id": ObjectId(parameter_id)}

            query_result = DB.query(query_dict=query_dict, collection_name="parameters")

            result = {"database": DB_NAME,
                      "collection": "parameters",
                      "parameters": query_result}

            query_dict = {"parameter_id": ObjectId(parameter_id)}

            database = DB.get_database()
            for col_name in database.list_collection_names():
                output = database[col_name].find(query_dict)

                count = output.count()
                if count > 0:
                    result["shoppers_collection_name"] = col_name
                    return result

            return result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@NAME_SPACE.route('/<string:parameter_id>/shoppers')
class ParameterItemShopper(Resource):
    """Shoppers generated from a set of parameters"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'parameter_id': 'Parameter ID used to retrieve the set of '
                                     'parameters used to generate the mock shopper data',
                     'limit': {'description': 'amount of documents to return '
                                              '(default: 50, min: 10, max: 200)',
                               'in': 'query',
                               'type': 'int',
                               'default': 50}
                     }
             )
    def get(self, parameter_id):
        """
        Returns the shoppers generated by a specific set of parameters
        :param parameter_id: the parameter id used to generate a set of shoppers
        :return: a dictionary of the shoppers that were generated by a specific
        set of parameters
        """
        try:
            query_dict = {"parameter_id": ObjectId(parameter_id)}
            limit = int(request.args.get('limit'))
            limit = max(min(limit, 50), 10)

            # prepare to run query on every collection in the database.
            result = {'database_name': DB_NAME, 'parameter_id': parameter_id,
                      'collections': {}}

            # run the query and format the output, then return the result.
            result = DB.db_query(query_dict, result, limit)
            return result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


NAME_SPACE = API.namespace('shoppers', description='Shoppers generated from a set of parameters')

SHOPPER_MODEL = API.model('Shopper', {
    "_id": fields.Integer,
    'Date': fields.Date(dt_format='iso8601'),
    'DayOfWeek': fields.String,
    'TimeIn': fields.DateTime(dt_format="iso8601"),
    'TimeSpent': fields.Float,
    'IsSenior': fields.Boolean,
    'IsSunny': fields.Boolean
})

SHOPPER_QUERY = {"Date": {"$gte": None, "$lte": None},
                 "IsSenior": None,
                 "IsSunny": None}


# noinspection PyUnresolvedReferences
@NAME_SPACE.route('/<string:collection_name>')
class ShopperCollection(Resource):
    """Represents shoppers"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument'},
             params={
                 'collection_name': 'Name of the collection with shopper data to be retrieved',
                 'startDate': {'description': 'start date to collect shoppers from '
                                              '(YYYY-MM-DD)',
                               'in': 'query',
                               'type': 'string',
                               'format': 'date-time'},
                 'endDate': {'description': 'start date to collect shoppers from '
                                            '(YYYY-MM-DD)',
                             'in': 'query',
                             'type': 'string',
                             'format': 'date-time'},
                 'isSenior': {'description': 'shoppers collected are seniors '
                                             '(True or False)',
                              'in': 'query',
                              'type': 'boolean'},
                 'isSunny': {'description': 'shoppers collected will be from sunny days '
                                            '(True or False)',
                             'in': 'query',
                             'type': 'boolean'},
                 'limit': {'description': 'amount of documents to return '
                                          '(default: 50, min: 10, max: 200)',
                           'in': 'query',
                           'type': 'int',
                           'default': 50}
             })
    def get(self, collection_name):
        """
        Returns a dictionary of all shoppers in the MongoDB database collection.
        :param collection_name: name of the collection in the database.
        :return: a dictionary of all documents in the MongoDB database collection.
        """

        if collection_name == "parameters":
            NAME_SPACE.abort(400, status="This URL should not be used to "
                                         "retrieve parameter information", statusCode="400")

        try:
            query_dict = dict(SHOPPER_QUERY)
            start_date = request.args.get('startDate')
            end_date = request.args.get('endDate')
            is_senior = boolean(request.args.get('isSenior'))
            is_sunny = boolean(request.args.get('isSunny'))
            limit = int(request.args.get('limit'))

            if start_date is None or end_date is None:
                query_dict.pop("Date")
            else:
                start_date, end_date = check_dates(start_date, end_date)
                query_dict['Date']['$gte'] = start_date
                query_dict['Date']['$lte'] = end_date

            if is_senior is None:
                query_dict.pop("IsSenior")
            else:
                query_dict["IsSenior"] = is_senior

            if is_sunny is None:
                query_dict.pop("IsSunny")
            else:
                query_dict["IsSunny"] = is_sunny

            print(query_dict)

            result = {"database": DB_NAME,
                      "collection": collection_name,
                      "shoppers": list(DB.query(query_dict=query_dict,
                                                collection_name=collection_name, limit=limit))}

            return result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @API.expect(SHOPPER_MODEL)
    @API.marshal_with(SHOPPER_MODEL, code=201)
    def post(self, collection_name):
        """
        Creates a shopper document in the specified collection
        :return: a message stating the status of the response
        """
        payload = API.payload
        shopper_id = payload["_id"]
        date = payload["Date"]
        day_of_week = payload["DayOfWeek"]
        time_in = payload["TimeIn"]
        time_spent = payload['TimeSpent']
        is_senior = payload["IsSenior"]
        is_sunny = payload["IsSunny"]
        message = ''

        try:
            date = datetime.strptime(payload['Date'], "%Y-%m-%d")
        except ValueError:
            message += "Invalid Date {}. ".format(date)

        try:
            time_in = parser.isoparse(time_in)
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
            return message, 404

        shopper_dict = {"_id": shopper_id, "Date": date, "DayOfWeek": day_of_week,
                        "TimeIn": time_in, "TimeSpent": time_spent,
                        "IsSenior": is_senior, "IsSunny": is_sunny}

        try:
            DB.add_document(shopper_dict, collection_name=collection_name)
            msg = "Successfully added a shopper to " + collection_name
            msg += " collection in " + DB_NAME + " database."
            return msg, 200

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=POST_STATUS, statusCode="500")
        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=POST_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@NAME_SPACE.route("/<string:collection_name>/<int:shopper_id>")
class ShopperItem(Resource):
    """Represents a shopper"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument'},
             params={
                 'collection_name': 'Name of the collection with shopper data to be retrieved',
                 'shopper_id': 'ID of the shopper whose data will be retrieved'})
    def get(self, collection_name, shopper_id):
        """
        Returns a dictionary with information about the shopper with the specified ID.
        :param collection_name: name of the collection in the database.
        :param shopper_id: id of the shopper.
        :return: a dictionary with information about the shopper with the specified ID.
        """
        try:
            query_dict = {"ShopperId": shopper_id}
            result = {"database": DB_NAME,
                      "collection": collection_name,
                      "shopper": DB.query(query_dict=query_dict, collection_name=collection_name)}

            return result

        except KeyError as err:
            NAME_SPACE.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            NAME_SPACE.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


if __name__ == '__main__':
    APP.run(debug=True)
