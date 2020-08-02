"""Shopper API for accessing shopper data in MongoDB."""

from datetime import datetime
from calendar import day_name
from flask import Flask, request
from flask_restx import Api, Resource
from bson import ObjectId

from shoppermodel import ShopperDatabase

APP = Flask(__name__)
API = Api(APP, title='Shopper API', description='Access generated mock shopper data')

DB = ShopperDatabase()
DB_NAME = "shoppers_db"
DB.connect_to_client(database_name=DB_NAME)


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


"""
Implemented Flask-RestPLUS and Swagger UI by referring to
https://morioh.com/p/7c1ce2462a74
"""

GET_STATUS = "Could not retrieve information"

name_space = API.namespace('collections', description='Collections in the MongoDB database')


@name_space.route("")
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
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


name_space = API.namespace('parameters', description='Parameters used to '
                                                     'generate the mock shopper data')


@name_space.route("")
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
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@name_space.route('/<string:parameter_id>')
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
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@name_space.route('/<string:parameter_id>/shoppers')
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
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


name_space = API.namespace('shoppers', description='Shoppers generated from a set of parameters')


# noinspection PyUnresolvedReferences
@name_space.route('/<string:collection_name>')
class ShopperCollection(Resource):
    """Represents shoppers"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument'},
             params={
                 'collection_name': 'Name of the collection with shopper data to be retrieved'})
    def get(self, collection_name):
        """
        Returns a dictionary of all shoppers in the MongoDB database collection.
        :param collection_name: name of the collection in the database.
        :return: a dictionary of all documents in the MongoDB database collection.
        """

        if collection_name == "parameters":
            name_space.abort(400, status="This URL should not be used to "
                                         "retrieve parameter information", statusCode="400")

        try:
            result = {"database": DB_NAME,
                      "collection": collection_name,
                      "shoppers": list(DB.query(query_dict={}, collection_name=collection_name))}

            return result

        except KeyError as err:
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@name_space.route("/<string:collection_name>/<int:shopper_id>")
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
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


# noinspection PyUnresolvedReferences
@name_space.route("/<string:start_date>/<string:end_date>")
class ShopperCollectionDate(Resource):
    """Represents a list of shoppers during a range of dates"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'start_date': 'Start date for the range of dates to select (ex. 2018-03-05)',
                     'end_date': 'End date for the range of dates to select (ex. 2018-05-05)'})
    def get(self, start_date, end_date):
        """
        Return a dictionary of the documents in the database with dates
        in range of given start and end dates. The start and end dates must be within
        3 months.
        :param start_date: start date for the range of dates to select (ex. 2018-03-05).
        :param end_date: end date for the range of dates to select (ex. 2018-04-10).
        :return: Return a dictionary of the documents in the database with dates
        in range of given start and end dates.
        """
        # check if start and end dates are valid.
        start, end = check_dates(start_date, end_date)
        if isinstance(start, str):
            return start, 404

        try:
            # prepare to run query on every collection in the database.
            query_dict = {"Date": {"$gte": start, "$lte": end}}
            result = {"start_date": start.strftime("%Y-%m-%d"),
                      "end_date": end.strftime("%Y-%m-%d"),
                      "database": DB_NAME,
                      "collections": {}
                      }

            # run the query and format the output, then return the result.
            result = DB.db_query(query_dict, result)
            return result

        except KeyError as err:
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


URL = "/<string:is_senior>/<string:start_date>/<string:end_date>"


@name_space.route(URL)
class SeniorShopper(Resource):
    """Return a dictionary of senior shoppers during a range of dates"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'is_senior': 'True if selecting senior shoppers, False otherwise',
                     'start_date': 'Start date for the range of dates to select (ex. 2018-03-05)',
                     'end_date': 'End date for the range of dates to select (ex. 2018-05-05)'})
    def get(self, is_senior, start_date, end_date):
        """
        Return a dictionary of documents in the database that are within
        the range of the provided start and end dates and is senior is set
        to true. The start and end dates must be within 3 months.
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
            return start, 404

        # check is_senior is a boolean value.
        is_senior = boolean(is_senior)
        if isinstance(is_senior, str):
            return is_senior, 404

        try:
            # prepare to run query on every collection in the database.
            query_dict = {"Date": {"$gte": start, "$lte": end}, "IsSenior": is_senior}
            result = {"start_date": start.strftime("%Y-%m-%d"),
                      "end_date": end.strftime("%Y-%m-%d"),
                      "is_senior": is_senior,
                      "database": DB_NAME,
                      "collections": {}
                      }

            # run the query and format the output, then return the result.
            result = DB.db_query(query_dict, result)
            return result

        except KeyError as err:
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


URL = "/<string:is_sunny>/"
URL += "<string:is_weekend>/<string:start_date>/<string:end_date>"


@name_space.route(URL)
class SunnyShopper(Resource):
    """Return a dictionary of sunny weekend shoppers during a range of dates"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'is_sunny': 'True if selecting sunny days, False otherwise',
                     'is_weekend': 'True if selecting weekends, False otherwise',
                     'start_date': 'Start date for the range of dates to select (ex. 2018-03-05)',
                     'end_date': 'End date for the range of dates to select (ex. 2018-05-05)'})
    def get(self, is_sunny, is_weekend, start_date, end_date):
        """
        Return a dictionary of selected documents in the database. The documents
        are within the range of the provided start and end dates and the the shopper
        visited the store on a sunny or not sunny weekend or weekday.
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
            return start, 404

        # check if is_sunny is boolean.
        is_sunny = boolean(is_sunny)
        if isinstance(is_sunny, str):
            return is_sunny, 404

        # check if is_weekend is boolean.
        is_weekend = boolean(is_weekend)
        if isinstance(is_weekend, str):
            return is_weekend, 404

        try:
            # prepare to run query on every collection in the database.
            if is_weekend:
                query_dict = {"Date": {"$gte": start, "$lte": end},
                              "$or": [{"DayOfWeek": "Saturday"}, {"DayOfWeek": "Sunday"}],
                              "IsSunny": is_sunny,
                              }
                result = {"start_date": start.strftime("%Y-%m-%d"),
                          "end_date": end.strftime("%Y-%m-%d"),
                          "DayOfWeek": ["Saturday, Sunday"],
                          "IsSunny": is_sunny,
                          "database": DB_NAME,
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
                          "database": DB_NAME,
                          "collections": {}
                          }

            # run the query and format the output, then return the result.
            result = DB.db_query(query_dict, result)
            return result

        except KeyError as err:
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")


POST_STATUS = "Could not save information"
URL = "/<string:collection_name>/<int:shopper_id>/"
URL += "<string:date>/<string:day_of_week>/"
URL += "<string:time_in>/<int:time_spent>/<string:is_senior>/<string:is_sunny>"
parameters = {"collection_name": "Name of the MongoDB collection to add a new shopper into",
              "shopper_id": "ID for the new shopper to be added",
              "date": "The date when the shopper visited the store",
              "day_of_week": "The day of week the shopper visited the store",
              "time_in": "The time that the shopper came into the store",
              "time_spent": "The time that the shopper spent in the store (in minutes)",
              "is_senior": "True if the shopper is a senior, false otherwise",
              "is_sunny": "True if the day that the shopper visited was sunny, false otherwise"}


@name_space.route(URL, methods=["POST"])
class Shopper(Resource):
    """Adds a shopper"""

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params=parameters)
    def post(self, collection_name, shopper_id, date, day_of_week,
             time_in, time_spent, is_senior, is_sunny):
        """
        Adds a document to the specified MongoDB database collection
        with provided information.
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
            name_space.abort(500, err.__doc__, status=POST_STATUS, statusCode="500")
        except Exception as err:
            name_space.abort(400, err.__doc__, status=POST_STATUS, statusCode="400")


if __name__ == '__main__':
    APP.run(debug=True)
