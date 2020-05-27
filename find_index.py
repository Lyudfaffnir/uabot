import requests
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


def get_table_on_page(num):
    if num == 0:
        return "Index not found, please enter the streetname using the cyrillic alphabet"
    else:
        # kyiv_index_url = "http://indexua.net/kievzipindex/" + str(num) + "/"
        kyiv_index_url = "https://tkiev.com/pochtovye-indeksy-kieva.php"
        response = requests.get(kyiv_index_url)
        html_text = response.text

        soup = BeautifulSoup(html_text, 'html.parser')
        table = soup.find("div", class_="nv-content-wrap entry-content")
        x = table.table.tbody.prettify()
        print(x)

        return 'popa'


print(get_table_on_page(9))
#get_table_on_page(example1)
#get_table_on_page(example2)