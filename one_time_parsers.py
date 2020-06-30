import requests
from bs4 import BeautifulSoup

# THIS DOCUMENT CONTAINS PARSERS WHICH ARE USED ONE TIME
# TO RECEIVE THE DATA FROM WEBSITE AND ADD IT TO THE MONGODB


# THIS FUNCTION IS NOT USED ANYMORE
# def find_the_page(street):
#    finder = street[0]
#    num = 0
#    try:
#        int(finder)
#        print("the first argument is an integer")
#    except ValueError:
#        print('The first argument is not integer')
#        alphabet = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К",
#                    "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф",
#                    "Ц", "Ч", "Ш", "Щ", "Э", "Ю", "Я"]
#        if finder.upper() in alphabet:
#            for i in range(0, 29):
#                if alphabet[i] == finder.upper():
#                    num = i + 2
#       else:
#            print("This street does not exist")
#            num = 0
#    finally:
#        return num


# KYIV
def parse_kyiv_addresses():
    kyiv_index_url = "https://tkiev.com/pochtovye-indeksy-kieva.php"
    response = requests.get(kyiv_index_url)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')
    area = soup.find("div", class_="theiaPostSlider_preloadedSlide")
    info = area.table.tbody.find_all("tr")
    dictionary_info = {}
    increment = 0
    for i in info:
        address = i.td.string
        address = str(address).strip()
        index = i.td.findNext("td")
        if index:
            index = str(index.string).strip()
            index = "0" + index
        else:
            index = ""
        dickid = "id" + str(increment)
        dictionary_info.update({dickid: {"address": address, "index": index, "city": "Kyiv"}})
        increment = increment + 1
    return dictionary_info


# ======== FIND INDEX BY ADDRESS IN DICTIONARY =====
# This function is not used anymore. Was used previously, when the data was not on the MongoDB
# and therefore each time as the user requested data it was parsed again. Was removed due to insecurity.
def get_data_from_dictionary(dictionary, request):
    new_string = ""
    for i in dictionary:
        address = dictionary.get(i).get("address")
        index = dictionary.get(i).get("index")
        if request.upper() in str(address.upper()):
            new_string += f"\n{address}: {index}"
    return new_string
