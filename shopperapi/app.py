"""Shopper API for accessing shopper data in MongoDB."""

from datetime import datetime
from dateutil import parser
from calendar import day_name
from flask import Flask, request
from flask_restx import Api, Resource, fields
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

shopper_model = API.model('Shopper', {
    "_id": fields.Integer,
    'Date': fields.Date(dt_format='iso8601'),
    'DayOfWeek': fields.String,
    'TimeIn': fields.DateTime(dt_format="iso8601"),
    'TimeSpent': fields.Float,
    'IsSenior': fields.Boolean,
    'IsSunny': fields.Boolean
})

shopper_query = {"Date": {"$gte": None, "$lte": None},
                 "IsSenior": None,
                 "IsSunny": None}


# noinspection PyUnresolvedReferences
@name_space.route('/<string:collection_name>')
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
            name_space.abort(400, status="This URL should not be used to "
                                         "retrieve parameter information", statusCode="400")

        try:
            query_dict = dict(shopper_query)
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
                      "shoppers": list(DB.query(query_dict=query_dict, collection_name=collection_name, limit=limit))}

            return result

        except KeyError as err:
            name_space.abort(500, err.__doc__, status=GET_STATUS, statusCode="500")

        except Exception as err:
            name_space.abort(400, err.__doc__, status=GET_STATUS, statusCode="400")

    @API.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @API.expect(shopper_model)
    @API.marshal_with(shopper_model, code=201)
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
        print(shopper_dict)

        try:
            DB.add_document(shopper_dict, collection_name=collection_name)
            msg = "Successfully added a shopper to " + collection_name
            msg += " collection in " + DB_NAME + " database."
            return msg, 200

        except KeyError as err:
            name_space.abort(500, err.__doc__, status=POST_STATUS, statusCode="500")
        except Exception as err:
            name_space.abort(400, err.__doc__, status=POST_STATUS, statusCode="400")


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


if __name__ == '__main__':
    APP.run(debug=True)
