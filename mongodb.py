import personal_data
from pymongo import MongoClient


def create_connection():
    connection_string = "mongodb+srv://" + str(personal_data.get_login()) + ":" + str(personal_data.get_password()) + "@petprojectsx-c0xb2.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client.uabot
    return db


def insert_dictionary(dictionary):
    db = create_connection()
    indexxxes = db.indexes
    indexxxes.insert_one(dictionary)
    return "OK"


def receive_backup():
    db = create_connection()
    return db.indexes
