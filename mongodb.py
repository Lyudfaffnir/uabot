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
    city_latina = db.index_data.distinct("city_latina")
    dictionary = {}
    iterator = 0
    for i in city_cyrillic:
        j = city_latina[iterator]
        dictionary.update({i: j})
        iterator += 1
    return dictionary
