import json
from pymongo import MongoClient

def get_login():
    with open("config.json", "r") as config:
        config = json.loads(config.read())
        login = str(config['mongo_login'])
        return login

def get_password():
    with open("config.json", "r") as config:
        config = json.loads(config.read())
        password = str(config['mongo_pass'])
        return password


# Basic MongoDB access
def mongo_get_db():
    connection_string = "mongodb+srv://" + get_login() + ":" + get_password() +\
                        "@petprojectsx-c0xb2.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client.uabot
    return db


# ==== MONGO INTERACTION WITH BOT ====

# Searches index by input
def mongo_get_index(user_input, city):
    print(user_input)
    db = mongo_get_db()
    cursor = db.index_data.find({"city": str(city)})
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
    city_cyrillic = db.index_data.distinct("city")
    # city_latina = db.index_data.distinct("city_latina")
    cities_list = []
    for i in city_cyrillic:
        cities_list.append(i)
    return cities_list
