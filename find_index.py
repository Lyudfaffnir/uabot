import requests
import mongodb
from bs4 import BeautifulSoup

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


def get_table_on_page():
    # kyiv_index_url = "http://indexua.net/kievzipindex/" + str(num) + "/"
    kyiv_index_url = "https://tkiev.com/pochtovye-indeksy-kieva.php"
    response = requests.get(kyiv_index_url)
    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')
    area = soup.find("div", class_="nv-content-wrap entry-content")
    info = area.table.tbody.find_all("tr")
    dictionary_info = {}
    for i in info:
        address = i.td.string
        address = str(address).strip()
        index = i.td.findNext("td")
        if index:
            index = str(index.string).strip()
        else:
            index = ""
        dictionary_info.update({"address": address, "index": index})
    return dictionary_info


mongodb.add_dictionary(get_table_on_page())
