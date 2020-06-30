import logging
import personal_data
from mongodb import mongo_get_index, mongo_receive_cities
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
import emojis

# Global variables
current_city = ""
alphabet = "Cyrillic"
page = 1

# Basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Interaction with Mongo Functions
# TODO: Needs to be separated in the future
# TODO: Should show no more than 10 cities and footer interaction
def construct_cities_list():
    cities_list = mongo_receive_cities()
    keyboard = []
    # test list
    cities_list = ["London", "Kyiv", "Astana", "Lugansk", "ZP", "Kharkiv", "Donetsk", "Rio", "LA", "NY", "Atlanta"]
    list_len = len(cities_list)
    if list_len < 10 or list_len == 10:
        for city in cities_list:
           keyboard.append([InlineKeyboardButton(str(city), callback_data=str(city))])
    elif list_len > 10:
        global page
        last_index = page * 10
        first_index = last_index - 10
        page_list = cities_list[first_index:last_index]
        for city in page_list:
            keyboard.append([InlineKeyboardButton(str(city), callback_data=str(city))])
        prev_page_button = InlineKeyboardButton(emojis.encode(":arrow_left:"), callback_data="page_back")
        counter_button = InlineKeyboardButton(f"{last_index}/{list_len}", callback_data="do_nothing")
        next_page_button = InlineKeyboardButton(emojis.encode(":arrow_right:"), callback_data="page_forward")
        keyboard.append([prev_page_button, counter_button, next_page_button])
    return keyboard


def get_index(user_input, user_city):
    reply_string = ""
    if user_city == "":
        reply_string = personal_data.city_has_not_been_chosen
    else:
        our_indexes = mongo_get_index(user_input, user_city)
        if our_indexes == {}:
            reply_string = personal_data.nothing_found_string
        else:
            global current_city
            reply_string += personal_data.bingo + f"Город: {current_city}\n"
            for count, (key, value) in enumerate(our_indexes.items(), 1):
                reply_string += "\n<i>" + str(key) + "</i>: <b>" + str(value) + "</b>"
    return reply_string


# ==== Command Handlers ====
# "/start" handler
def start_command(update, context):
    reply_markup = InlineKeyboardMarkup(construct_cities_list())
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.start_string,
                             reply_markup=reply_markup)


# "/city" handler
def city_command(update, context):
    reply_markup = InlineKeyboardMarkup(construct_cities_list())
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.choose_city_string,
                             reply_markup=reply_markup)


# inline query handler
# By default chooses the city
def button_command(update, context):
    query = update.callback_query
    query.answer()
    global page
    if str(query.data) == "page_back":
        if page == 1:
            pass
        else:
            page = page - 1
            reply_markup = InlineKeyboardMarkup(construct_cities_list())
            context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.choose_city_string,
                                     reply_markup=reply_markup)
    elif str(query.data) == "page_forward":
        page += 1
        reply_markup = InlineKeyboardMarkup(construct_cities_list())
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.choose_city_string,
                                 reply_markup=reply_markup)
    else:
        global current_city
        current_city = str(query.data)
        query.edit_message_text(text=personal_data.city_is_chosen)


# text_handler
# By default needs to search for index by user input
def index_command(update, context):
    user_input = str(update.message.text)
    global current_city
    user_city = str(current_city)
    reply_string = get_index(user_input, user_city)
    print(reply_string)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_string, parse_mode=ParseMode.HTML)


# "/help" handler
# Is a requirement of Telegram API
def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.help_string,
                             parse_mode=ParseMode.HTML)


# "/find_city <user input>" handler
# TODO: Create search by city
def find_city_command(update, context):
    pass


# ==== MAIN METHOD ====
# Contains Command Handlers
def main():
    # Create updater
    updater = Updater(token=personal_data.token, use_context=True)
    dispatcher = updater.dispatcher
    # "/start" command
    start_handler = CommandHandler('start', start_command)
    dispatcher.add_handler(start_handler)
    # "/city" command
    choose_city_handler = CommandHandler('city', city_command)
    dispatcher.add_handler(choose_city_handler)
    # Here we receive the response from the inline query
    updater.dispatcher.add_handler(CallbackQueryHandler(button_command))
    # "/help" command
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    # How we handle each other text received
    text_handler = MessageHandler(Filters.text & (~Filters.command), index_command)
    dispatcher.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
