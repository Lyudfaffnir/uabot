import personal_data
from pymongo import MongoClient
import one_time_parsers


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
        if i == len(dictionary) + 1:
            break
        this_id = "id" + str(i)
        item = dictionary[this_id]
        address = item["address"]
        index = item["index"]
        city = item['city']
        itemdictionary = {"address": address, "index": index, "city": city}
        index_data.insert_one(itemdictionary)
        i += 1
    return "OK"


def get_our_index(user_input):
    print(user_input)
    db = receive_database()
    cursor = db.index_data.find({})
    addresses_i_found = ""
    for document in cursor:
        address = str(document['address'])
        # print(address.upper())
        # print(user_input.upper())
        index = str(document["index"])
        if user_input.upper() in address.upper():
            addresses_i_found += f"\n{address}: {index}"
    return str(addresses_i_found)

