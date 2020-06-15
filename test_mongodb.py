# source of all code on this page is from W3 Schools Tutorial for MongoDB:
# https://www.w3schools.com/python/python_mongodb_getstarted.asp
import pymongo  # use pip to install or conda install -c anaconda pymongo

"""
----------------------
| MongoDB    | SQL    |
----------------------
| Collection | Table  |
----------------------
| Document   | Record |
----------------------

Please install MongoDB Community Server and pymongo to run this file.
MongoDB Community Server Installation
Instructions: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
Installation File: https://www.mongodb.com/try/download/community
MongoDB Tutorial: https://www.linkedin.com/learning/learning-mongodb/install-mongodb-for-windows
MongoDB with Python Tutorial: 
  - recommend W3 Schools Tutorial https://www.w3schools.com/python/python_mongodb_getstarted.asp
  - LinkedIn Learning video: https://www.linkedin.com/learning/polyglot-web-development/understanding-python
"""

# Create a MongoClient Object and specify a connection URL
my_client = pymongo.MongoClient("mongodb://localhost:27017/")

# Connect to a database (MongoDB will create, if it doesn't exist)
my_db = my_client["my_database"]

# Delete "customers" collection if it exists
col_list = my_db.list_collection_names()
if "customers" in col_list:
    my_db["customers"].drop()

# Create a collection called "customers"
my_col = my_db["customers"]

# Insert a record in the "customers" collection.
my_dict = {"name": "John", "address": "Highway 37"}
x = my_col.insert_one(my_dict)

# Return the _id field
print(x.inserted_id)

# MongoDB doesn't create the database until a collection/table with at
# least one document/record has been added to the database.
print(my_client.list_database_names())

# Check if my_database exists
db_list = my_client.list_database_names()
if "my_database" in db_list:
    print("The database exists.")

# List all collections in the connected database
print(my_db.list_collection_names())

# Check if the "customers" collection exists
col_list = my_db.list_collection_names()
if "customers" in col_list:
    print("The collection exists.")

# Insert Multiple Documents
my_list = [
    {"name": "Amy", "address": "Apple st 652"},
    {"name": "Hannah", "address": "Mountain 21"},
    {"name": "Michael", "address": "Valley 345"},
    {"name": "Sandy", "address": "Ocean blvd 2"},
    {"name": "Betty", "address": "Green Grass 1"},
    {"name": "Richard", "address": "Sky st 331"},
    {"name": "Susan", "address": "One way 98"},
    {"name": "Vicky", "address": "Yellow Garden 2"},
    {"name": "Ben", "address": "Park Lane 38"},
    {"name": "William", "address": "Central st 954"},
    {"name": "Chuck", "address": "Main Road 989"},
    {"name": "Viola", "address": "Sideway 1633"}
]

x = my_col.insert_many(my_list)

# print list of the _id values of the inserted documents
print("\nPrint list of the _id values of the inserted documents")
print(x.inserted_ids)

# Insert multiple documents with specified IDs
print("\nInserting multiple documents with specified IDs")
my_list = [
    {"_id": 1, "name": "John", "address": "Highway 37"},
    {"_id": 2, "name": "Peter", "address": "Lowstreet 27"},
    {"_id": 3, "name": "Amy", "address": "Apple st 652"},
    {"_id": 4, "name": "Hannah", "address": "Mountain 21"},
    {"_id": 5, "name": "Michael", "address": "Valley 345"},
    {"_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
    {"_id": 7, "name": "Betty", "address": "Green Grass 1"},
    {"_id": 8, "name": "Richard", "address": "Sky st 331"},
    {"_id": 9, "name": "Susan", "address": "One way 98"},
    {"_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
    {"_id": 11, "name": "Ben", "address": "Park Lane 38"},
    {"_id": 12, "name": "William", "address": "Central st 954"},
    {"_id": 13, "name": "Chuck", "address": "Main Road 989"},
    {"_id": 14, "name": "Viola", "address": "Sideway 1633"}
]

x = my_col.insert_many(my_list)

# print list of the _id values of the inserted documents
print("\nPrint list of the _id values of the inserted documents")
print(x.inserted_ids)

# Find the first document in the customers collection:
print("\nFind the first document in the customers collection")
x = my_col.find_one()

print(x)

# Find/return all documents in the "customers" collection and print each document
print("\nFind all documents in customers collection and print each one")
for x in my_col.find():
    print(x)

# Return only some fields.
# Do not mix 0's and 1's unless the mix is caused by the _id field.
print("\nReturn only name and address")
for x in my_col.find({}, {"_id": 0, "name": 1, "address": 1}):
    print(x)

# Return all fields except the listed fields.
# Do not list any fields that should be included.
print("\nReturn all fields except addresses")
for x in my_col.find({}, {"address": 0}):
    print(x)

# Filter the result.
# Find documents with the addres "Park Lane 38"
print("\nFilter")
my_query = {"address": "Park Lane 38"}

my_doc = my_col.find(my_query)

for x in my_doc:
    print(x)

# Advanced Query.
# To make advanced queries, use modifiers as values in the query object.
# Ex. To find the documents where the "address" field starts with
# the letter "S" or higher (alphabetically), use the greater than modifier: {"$gt": "S"}
print("\nAdvanced Query")
my_query = {"address": {"$gt": "S"}}

my_doc = my_col.find(my_query)

for x in my_doc:
    print(x)

# Filter strings with Regular Expressions
# To find the documents where the "address" field starts with the letter "S",
# use the regular expression {"$regex": "^S"}
print("\nFilter with Regular Expression")
my_query = {"address": {"$regex": "^S"}}

my_doc = my_col.find(my_query)

for x in my_doc:
    print(x)

# Sort the result alphabetically by name (ascending)
print("\nSort by name in ascending order")
my_doc = my_col.find().sort("name")

for x in my_doc:
    print(x)

# Sort the result alphabetically by name (descending)
print("\nSort by name in descending order")
my_doc = my_col.find().sort("name", -1)

for x in my_doc:
    print(x)

# Update a document/record using update_one
# Change the address from "Valley 345" to "Canyon 123"
# 1st parameter: a query object defining which document to update (grabs 1st record queried)
# 2nd parameter: object defining the new values of the document
my_query = {"address": "Valley 345"}
new_values = {"$set": {"address": "Canyon 123"}}
print("\nUpdate a document")
my_col.update_one(my_query, new_values)

# print "customers" after the update
for x in my_col.find():
    print(x)

# Update all documents meeting the criteria of the query
# Update all documents where the address starts with the letter S
my_query = {"address": {"$regex": "^S"}}
new_values = {"$set": {"name": "Minnie"}}
print("\nUpdate a document")

x = my_col.update_many(my_query, new_values)

print(x.modified_count, " documents updated.")

# Limit the result in MongoDB
# 1 parameter: a number defining how many documents to return
print("\nLimit the results to only return 5 documents")
my_result = my_col.find().limit(5)

for x in my_result:
    print(x)

# Find documents with the address "Mountain 21" and
# delete only the first document.
print("\nFind documents with the address \"Mountain 21\" and delete only the first document.")
my_query = {"address": "Mountain 21"}

my_col.delete_one(my_query)

# Delete all documents where the address starts with the letter S
print("\nDelete all documents where the address starts with the letter S")
my_query = {"address": {"$regex": "^S"}}

x = my_col.delete_many(my_query)

print(x.deleted_count, " documents deleted.")

# Delete all documents in a collection
print("\nDelete all documents in a collection")
x = my_col.delete_many({})
print(x.deleted_count, " documents deleted.")
