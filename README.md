# MongoDB Tutorial

#### Mongo DB vs SQL Terminology
| **MongoDB**| **SQL**|
|:-----------|-------:|
| collection | table  |
| document   | record |

## Required Installations
Please install MongoDB Community Server and pymongo to run this file.

### MongoDB Community Server Installation
- [Instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
- [Installation File](https://www.mongodb.com/try/download/community)
- [MongoDB Installation Walkthrough + Tutorial Video](https://www.linkedin.com/learning/learning-mongodb/install-mongodb-for-windows)
- MongoDB with Python Tutorial: 
  - recommend [W3 Schools Tutorial](https://www.w3schools.com/python/python_mongodb_getstarted.asp)
  - [short LinkedIn Learning video](https://www.linkedin.com/learning/polyglot-web-development/understanding-python)

### Python Module PyMongo Installation
use pip to install or conda install -c anaconda pymongo

## Files in the Tutorial
- **test_mongodb.py**
  - runs all code snippets from [W3 Schools Tutorial](https://www.w3schools.com/python/python_mongodb_getstarted.asp)
- **convert_to_mongodb.py**
  - *set_up_mongodb(database_name, collection_name)*
    - sets up the MongoDB database
    - returns a tuple of the mongoDB database object and mongoDB collection object
  - *csv_to_mongodb(mongo_db_collection, csv_path)*
    - converts a csv to pandas data frame
    - converts the data frame to a records based dict (different formatting from dict used to create data frame)
    - add the new dictionary to the mongo_db_collection
    - this method took 19 seconds to run
  - *csv_to_json_to_mongodb(mongo_db_collection, csv_path)*
    - converts a csv to pandas data frame
    - converts the data frame to a records based json
    - add the new json to the mongo_db_collection
    - this method took 19 seconds to run