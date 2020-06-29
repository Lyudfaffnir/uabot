import personal_data
from pymongo import MongoClient


# Basic MongoDB access
def mongo_get_db():
    connection_string = "mongodb+srv://" + str(personal_data.get_login()) + ":" + str(personal_data.get_password()) +\
                        "@petprojectsx-c0xb2.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client.uabot
    return db


# ==== MONGO INTERACTION WITH BOT ====

# Searches index by input
def mongo_get_index(user_input, city):
    print(user_input)
    db = mongo_get_db()
    cursor = db.index_data.find({"city": city})
    addresses_i_found = {}
    for document in cursor:
        address = str(document['address'])
        index = str(document["index"])
        if user_input.upper() in address.upper():
            addresses_i_found.update({address: index})
    return addresses_i_found


# Get the values of "city" field
def mongo_receive_cities():
    db = mongo_get_db()
    cities_list = db.index_data.distinct("city")
    return cities_list


# ==== ONE-TIME FUNCTION ====
# MUST BE USED ONLY ONCE
def one_time_insert_dictionary(dictionary):
    db = mongo_get_db()
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
        item_dictionary = {"address": address, "index": index, "city": city}
        index_data.insert_one(item_dictionary)
        i += 1
    return "OK"
