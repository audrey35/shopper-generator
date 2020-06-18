"""
Research on Querying MongoDB.
"""

from datetime import datetime as dt
from convert_to_mongodb import set_up_mongodb
from convert_to_mongodb import csv_to_mongodb

# Set up MongoDB connection
my_db, my_col = set_up_mongodb()

# Load CSV data into MongoDB Collection
csv_to_mongodb(my_col)

start = dt.now()

print("\nLimit the results to only return 2 documents")
my_result = my_col.find().limit(2)

for x in my_result:
    print(x)

# Get data type of a field
# source: zetcode.com/python/pymongo
val = list(my_col.aggregate([{
    "$project": {
        "_id": 1,
        "all": {"$type": "$Date"}
    }
}]))
print("The type of Date column is {}".format(val[0]['all']))

val = list(my_col.aggregate([{
    "$project": {
        "_id": 1,
        "all": {"$type": "$TimeSpent"}
    }
}]))
print("The type of TimeSpent column is {}".format(val[0]['all']))

"""
# https://docs.mongodb.com/manual/reference/operator/aggregation/toDate/
# fail
my_col.aggregate([
    {"$addFields": {
        "convertedDate": {"$toDate": "$Date"}
    }}
])
# https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromString/
# fail
my_col.aggregate([{
    "$project": {
        "Date": {
            "$dateFromString": {
                "dateString": "$Date",
                "format": "%Y-%m-%d %H:%M:%S"
            }
        }
    }
}
])

val = list(my_col.aggregate([{
    "$project": {
        "_id": 1,
        "all": {"$type": "$Date"}
    }
}]))
print("The type of Date column is {}".format(val[0]['all']))"""

# Query using datetime
# https://stackoverflow.com/a/11957746
start2 = dt.strptime('2020-01-01', '%Y-%m-%d')
end = dt.strptime('2020-05-25', '%Y-%m-%d')
query = {"Date": {"$gte": start2, "$lte": end}}
date_query = my_col.find(query)
print("\nSelected {} rows between 2020-01-01 and 2020-05-25".format(my_col.count_documents(query)))
print("First five rows of {} are:".format(date_query.count()))
for x in date_query.limit(5):
    print(x)

# Query range of values
starting = 10
end = 20
query = {"TimeSpent": {"$gte": starting, "$lte": end}}
spent_query = my_col.find(query)
print("\nSelected {} rows between 10 and 20".format(my_col.count_documents(query)))
print("First five rows of {} are:".format(spent_query.count()))
for x in spent_query.limit(5):
    print(x)

# Query multiple fields
# https://stackoverflow.com/a/14928646
query = {"$or": [
    {"Date": start2},
    {"TimeSpent": {"$gte": starting, "$lte": end}}
]}
multi_query = my_col.find(query)
print("\nSelected {} rows based on Date and TimeSpent".format(my_col.count_documents(query)))
print("First five rows of {} are:".format(multi_query.count()))
for x in multi_query.limit(5):
    print(x)

# Query contains string: dates between January 2020
# source https://stackoverflow.com/a/38900769
query = {"Date": {"$regex": "2020-01", "$options": "i"}}
print("\nSelected {} rows between 2020-01-01 and 2020-01-31".format(my_col.count_documents(query)))
queried = my_col.find(query)
print("First five rows are:")
for x in queried.limit(5):
    print(x)

# Query equality condition
query = {"DayOfWeek": "Tuesday"}
queried = my_col.find(query)
print("Query DayOfWeek = Tuesday:")
for x in queried.limit(5):
    print(x)

print("Time taken to query MongoDB: {}".format(dt.now() - start))
