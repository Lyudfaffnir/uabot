import logging
import text
import json
from mongodb import mongo_get_index, mongo_receive_cities
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
import emojis

# TODO: Default_city = Киев
# Global variables
_cached_city = ""
_cached_city_page = 1

_cached_index_page = 0
_cached_index_dict = {}

def get_token():
    with open("config.json", "r") as config:
        config = json.loads(config.read())
        token = str(config['token'])
        return token


# Basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Interaction with Mongo Functions
# TODO: Needs to be separated in the future
def construct_cities_list(cities_list, page_num):
    keyboard = []
    list_len = len(cities_list)
    buttons_per_page = 5
    if list_len <= buttons_per_page:
        for city in cities_list:
            keyboard.append([InlineKeyboardButton(str(city), callback_data=str(city))])

    else:
        # compute first and last indexes
        last_index = page_num * buttons_per_page
        first_index = last_index - buttons_per_page

        # extract the cities for the page
        page_list = cities_list[first_index:last_index]

        # add cities
        for city in page_list:
            keyboard.append([InlineKeyboardButton(str(city), callback_data=str(city))])

        # add navigation footer
        navigation_footer = [InlineKeyboardButton(emojis.encode(":arrow_left:"), callback_data="page_back"),
                             InlineKeyboardButton(f"{last_index}/{list_len}", callback_data="do_nothing"),
                             InlineKeyboardButton(emojis.encode(":arrow_right:"), callback_data="page_forward")]
        keyboard.append(navigation_footer)
    return keyboard


def get_index(user_input, user_city):
    if user_city == "":
        reply = text.txt_city_empty
    else:
        global _cached_index_dict
        our_indexes = mongo_get_index(user_input, user_city)
        _cached_index_dict = our_indexes
        global _cached_city

        if not our_indexes:
            reply = text.txt_index_not_found

        else:
            this_page = int(0)
            try:
                addresses = list(_cached_index_dict.keys())
                indexes = list(_cached_index_dict.values())
                reply = ''
                reply += text.txt_bingo + f"Город: {user_city}\n"
                for x in range(this_page * 10, this_page + 10):
                    reply += f"\n<i>{str(addresses[x])}</i>: <b>{str(indexes[x])}</b>"
            except TypeError:
                reply = text.txt_error
    return reply

# ==== Command Handlers ====
# "/start" handler
def start_command(update, context):
    reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), 1))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_start,
                             reply_markup=reply_markup)


# "/city" handler
def city_command(update, context):
    reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), 1))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_available_cities,
                             reply_markup=reply_markup)


# inline query handler
# By default chooses the city
def inline_query_handler(update, context):
    query = update.callback_query
    query.answer()
    global _cached_city_page
    if str(query.data) == "page_back":
        if _cached_city_page <= 1:
            reply = text.txt_zero_page
        else:
            _cached_city_page -= 1
            reply = text.txt_available_cities
        reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), _cached_city_page))
        query.edit_message_text(text=reply, reply_markup=reply_markup)

    elif str(query.data) == "page_forward":
        _cached_city_page += 1
        reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), _cached_city_page))
        query.edit_message_text(text=text.txt_available_cities, reply_markup=reply_markup)

    else:
        global _cached_city
        _cached_city = str(query.data)
        query.edit_message_text(text=text.txt_city_found)


# text_handler
# By default needs to search for index by user input
def index_command(update, context):
    user_input = str(update.message.text)
    global _cached_city
    user_city = str(_cached_city)
    reply_string = get_index(user_input, user_city)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_string,
                             parse_mode=ParseMode.HTML)


# "/help" handler
# Is a requirement of Telegram API
def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_help,
                             parse_mode=ParseMode.HTML)


# "/find_city <user input>" handler
def find_city_command(update, context):
    cities = mongo_receive_cities()
    try:
        if not context.args:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_no_input,
                                     parse_mode=ParseMode.HTML)

        else:
            _input = ''
            for word in context.args:
                _input += word
            reply_list = []
            for city in cities:
                if _input.upper() in city.upper():
                    reply_list.append(city)
            if not reply_list:
                context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_no_reply,
                                         parse_mode=ParseMode.HTML)
            else:
                keyboard_reply = InlineKeyboardMarkup(construct_cities_list(reply_list, 1))
                context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_cities_received,
                                         reply_markup=keyboard_reply)
    except TypeError:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text.txt_error)


# Contains Command Handlers
def main():
    # Create updater
    updater = Updater(token=get_token(), use_context=True)
    dispatcher = updater.dispatcher
    # "/start" command
    start_handler = CommandHandler('start', start_command)
    dispatcher.add_handler(start_handler)
    # "/city" command
    choose_city_handler = CommandHandler('city', city_command)
    dispatcher.add_handler(choose_city_handler)
    # Here we receive the response from the inline query
    dispatcher.add_handler(CallbackQueryHandler(inline_query_handler))
    # "/help" command
    dispatcher.add_handler(CommandHandler('help', help_command))
    # How we handle each other text received
    text_handler = MessageHandler(Filters.text & (~Filters.command), index_command)
    dispatcher.add_handler(text_handler)
    # "/find_city" command
    dispatcher.add_handler(CommandHandler('find_city', find_city_command))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
