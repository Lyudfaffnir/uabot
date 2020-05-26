import requests
from bs4 import BeautifulSoup


def find_the_page(street):
    finder = street[0]
    num = 0
    try:
        int(finder)
        print("the first argument is an integer")
    except ValueError:
        print('The first argument is not integer')
        alphabet = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К",
                    "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф",
                    "Ц", "Ч", "Ш", "Щ", "Э", "Ю", "Я"]
        if finder.upper() in alphabet:
            for i in range(0, 29):
                if alphabet[i] == finder.upper():
                    num = i + 2
        else:
            print("This street does not exist")
            num = 0
    finally:
        return num


example = find_the_page("Малевич")
example2 = find_the_page("Валевич")
example1 = find_the_page("Калевич")


def get_table_on_page(num):
    if num == 0:
        return "Index not found, please enter the streetname using the cyrillic alphabet"
    else:
        kyiv_index_url = "http://indexua.net/kievzipindex/" + str(num) + "/"
        response = requests.get(kyiv_index_url)
        html_text = response.text

        soup = BeautifulSoup(html_text, 'html.parser')
        table = soup.find("div", class_="content")
        print(soup.title.string.encode("utf-8"))

        return table


get_table_on_page(example)
get_table_on_page(example1)
get_table_on_page(example2)