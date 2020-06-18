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
"""
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
query = {"TimeSpent": {"$gte": 10, "$lte": 20}}
spent_query = my_col.find(query)
print("\nSelected {} rows between 10 and 20".format(my_col.count_documents(query)))
print("First five rows of {} are:".format(spent_query.count()))
for x in spent_query.limit(5):
    print(x)

# Query multiple fields
# https://stackoverflow.com/a/14928646
query = {"$or": [
    {"Date": start2},
    {"TimeSpent": {"$gte": 10, "$lte": 20}}
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


def query(query_dict={}, sort_dict={}, print_statement=""):
    if sort_dict == {} or isinstance(sort_dict) != dict:
        output = my_col.find(query_dict)
    else:
        output = my_col.find(query_dict).sort(sort_dict)
    print(print_statement, "count", output.count())
    for o in output.limit(5):
        print(o)


# Query equality condition
# SELECT * FROM shoppers WHERE DayOfWeek = "Tuesday"
q = {"DayOfWeek": "Tuesday"}
s = '\nSELECT * FROM shoppers WHERE DayOfWeek = "Tuesday"'
query(q, print_statement=s)

# Specify conditions using query operators
# SELECT * FROM shoppers WHERE DayOfWeek in ("Saturday", "Sunday")
q = {"DayOfWeek": {"$in": ["Saturday", "Sunday"]}}
s = '\nSELECT * FROM shoppers WHERE DayOfWeek in ("Saturday", "Sunday")'
query(q, print_statement=s)

# Specify AND conditions
# SELECT * FROM shoppers WHERE DayOfWeek = "Tuesday" AND IsSenior = True
q = {"DayOfWeek": "Tuesday", "IsSenior": True}
s = '\nSELECT * FROM shoppers WHERE DayOfWeek = "Tuesday" AND IsSenior = True'
query(q, print_statement=s)

# Specify OR conditions
# SELECT * FROM shoppers WHERE DayOfWeek = "Saturday" OR IsSenior = True
q = {"$or": [{"DayOfWeek": "Saturday"}, {"IsSenior": True}]}
s = '\nSELECT * FROM shoppers WHERE DayOfWeek = "Saturday" OR IsSenior = True'
query(q, print_statement=s)

# Specify AND as well as OR conditions
# SELECT * FROM shoppers WHERE DayOfWeek = "Saturday" AND
# ( IsSenior = True OR DayOfWeek = "Monday" )
q = {"DayOfWeek": "Saturday", "$or": [{"IsSenior": True}, {"DayOfWeek": "Monday"}]}
s = '\nSELECT * FROM shoppers WHERE DayOfWeek = "Saturday" AND ' \
    '( IsSenior = True OR DayOfWeek = "Monday" )'
query(q, print_statement=s)

# Query Range of Int
q = {"TimeSpent": {"$gt": 5, "$lt": 10}}
s = '\nSELECT * FROM shoppers WHERE TimeSpent BETWEEN 5 AND 10'
query(q, print_statement=s)

# Query Range of Dates
q = {"Date": {"$gt": dt(2020, 5, 10), "$lt": dt(2020, 5, 25)}}
s = '\nSELECT * FROM shoppers WHERE Date BETWEEN "2020-05-10" AND "2020-05-25"'
query(q, print_statement=s)

# Sort by TimeSpent (ascending = 1, descending = -1
q = {}
s = [("TimeSpent", 1), ("Date", -1)]
p = '\nSort by TimeSpent in ascending, then by Date in descending'
query(q, s, p)

# Sort by Time Spent (descending = -1)
q = {}
s = [("TimeSpent", -1)]
p = '\nSort by TimeSpent in descending'

a = [{"$match": {"DayOfWeek": "Sunday"}},
     {"$group": {"_id": "$Date", "count": {"$sum": 1}}},
     {"$sort": {"count": -1}}]
ag = my_col.aggregate(a)
print("\nOn a Sunday, ")
for e in ag:
    print(e)

print("Time taken to query MongoDB: {}".format(dt.now() - start))
