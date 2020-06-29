from mongodb import mongo_get_db


# ==== ONE-TIME FUNCTION ====
# MUST BE USED ONLY IN PYTHON CONSOLE!
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


def create_backup_collection():
    db = mongo_get_db()
    index_data3 = db.index_data3
    for document in db.index_data.find({}):
        index_data3.insert_one(document)
    return "OK"


def change_city_name_to_cyrillic():
    db = mongo_get_db()
    index_data = db.index_data
    index_data.update_many({'city': 'Kyiv'}, {"$set": {'city': 'Киев'}})
    return "ОК"


def add_latin_name():
    db = mongo_get_db()
    index_data = db.index_data
    index_data.update_many({'city': 'Бортничи'}, {"$set": {'city_latina': 'Bortnichi'}},)
    return "ОК"


def receive_bortnichi():
    db = mongo_get_db()
    index_data = db.index_data
    cursor = db.index_data.find({'address': {"$regex": "Бортничи"}})
    for doc in cursor:
        unique_id = doc["_id"]
        string = doc['address']
        new_string = string[:-9]

        index_data.update_one({'_id': unique_id}, {"$set": {'address': new_string}})
        pass


def delete_none_index():
    db = mongo_get_db()
    index_data = db.index_data
    index_data.delete_many({'index': '0None'})
