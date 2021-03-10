from pymongo import MongoClient
mongo_client = 'localhost:27017'
db_connection_check = MongoClient(mongo_client)
if not db_connection_check:
    print('Database Connection Failed')