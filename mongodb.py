import personal_data
from pymongo import MongoClient
import find_index


def receive_database():
    connection_string = "mongodb+srv://" + str(personal_data.get_login()) + ":" + str(personal_data.get_password()) + "@petprojectsx-c0xb2.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client.uabot
    return db


def insert_dictionary(dictionary):
    db = receive_database()
    index_data = db.index_data
    i = 1
    for x in dictionary:
        this_id = "id" + str(i)
        item = dictionary[this_id]
        address = item["address"]
        index = item["index"]
        city = item['city']
        itemdictionary = {"address": address, "index": index, "city": city}
        index_data.insert_one(itemdictionary)
        i += 1
    return "OK"


def receive_backup():
    db = receive_database()
    cursor = db.index_data.find({})
    for document in cursor:
        print(document)
    return cursor


insert_dictionary(find_index.parse_kyiv_addresses())
receive_backup()
