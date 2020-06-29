import logging
import personal_data
from mongodb import mongo_get_index, mongo_receive_cities
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler

# Global variables
current_city = ""
alphabet = "Cyrillic"

# Basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Interaction with Mongo Functions
# TODO: Needs to be separated in the future
# TODO: Should show no more than 10 cities and footer interaction
def construct_cities_list():
    cities_list = mongo_receive_cities()
    keyboard = []
    for count, (key, value) in enumerate(cities_list.items(), 1):
        if alphabet == 'Cyrillic':
            keyboard.append([InlineKeyboardButton(str(key), callback_data=str(key))])
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
