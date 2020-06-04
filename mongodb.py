import personal_data
from pymongo import MongoClient


def add_dictionary(dictionary):
    connection_string = "mongodb+srv://" + str(personal_data.get_login()) + ":" + str(personal_data.get_password()) + "@petprojectsx-c0xb2.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client.uabot
    indexxxes = db.indexes
    indexxxes.insert_one(dictionary)
    return 0


print(add_dictionary({"zhil": "faust"}))
