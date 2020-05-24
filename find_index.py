import requests
from bs4 import BeautifulSoup


def find_the_page(street):
    finder = street[0]
    num = 0
    try:
        int(finder)
        print("the first argument is an integer")
        num = 1
    except ValueError:
        print('The first argument is not integer')
        if finder.upper() == "А":
            num = 2
        elif finder.upper() == "Б":
            num = 3
        elif finder.upper() == "В":
            num = 4
        elif finder.upper() == "Г":
            num = 5
        elif finder.upper() == "Д":
            num = 6
        elif finder.upper() == "Е":
            num = 7
        elif finder.upper() == "Ж":
            num = 8
        elif finder.upper() == "З":
            num = 9
        elif finder.upper() == "И":
            num = 10
        elif finder.upper() == "К":
            num = 11
        elif finder.upper() == "Л":
            num = 12
        elif finder.upper() == "М":
            num = 13
        elif finder.upper() == "Н":
            num = 14
        elif finder.upper() == "О":
            num = 15
        elif finder.upper() == "П":
            num = 16
        elif finder.upper() == "Р":
            num = 17
        elif finder.upper() == "С":
            num = 18
        elif finder.upper() == "Т":
            num = 19
        elif finder.upper() == "У":
            num = 20
        elif finder.upper() == "Ф":
            num = 21
        elif finder.upper() == "Ц":
            num = 22
        elif finder.upper() == "Ч":
            num = 23
        elif finder.upper() == "Ш":
            num = 24
        elif finder.upper() == "Щ":
            num = 25
        elif finder.upper() == "Э":
            num = 26
        elif finder.upper() == "Ю":
            num = 25
        elif finder.upper() == "Я":
            num = 26
        else:
            num = 0
    finally:
        return num


example1 = find_the_page("Ломоносова")
example2 = find_the_page("8-го марта")


def parse_the_page(num):
    if num == 0:
        return "Index not found, please enter the streetname using the cyrillic alphabet"
    else:
        kyiv_index_url = "http://indexua.net/kievzipindex/" + str(num) + "/"
        response = requests.get(kyiv_index_url)
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser', from_encoding="utf-8")


parse_the_page(example1)
parse_the_page(example2)
