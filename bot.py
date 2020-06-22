import logging
import personal_data
from mongodb import get_our_index
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler

updater = Updater(token=personal_data.token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
city = ""


# ====== BOT START FUNCTION =====
# Should answer back with general specified information, such as "city" and "language"
# and the bot should set its settings depending on customer's answer. At the moment
# just response with the pre-generated text
# TODO: Set inline mode for choosing the city
def start(update, context):
    keyboard = [[InlineKeyboardButton("Киев", callback_data="Kyiv")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.start_string, reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    global city
    city = str(query.data)
    query.edit_message_text(text="Вы выбрали город {}".format(query.data))


# ========= TEST ECHO FUNCTION ===========
#  Was used to train echo_handler, does nothing at the moment, can be safely deleted
# def echo(update, context):
#    request = update.message.text
#    dict_indexes = find_index.get_table_on_page()
#    answer = find_index.get_data_from_dictionary(dict_indexes, request)
#    if answer == "":
#        answer = personal_data.nothing_found_string
#    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

# ====== DATABASE QUERY FUNCTION =========
# All the database-related functions can be found on the file mongodb.py. At the moment we have
# single collection with a single city, through which the query follows.
# TODO: Add the city parameter, so we can store information about several cities in a single collection.
def search_for_index_in_mongo(update, context):
    user_input = update.message.text
    global city
    user_city = city
    our_indexes = get_our_index(user_input, user_city)
    if our_indexes == "":
        our_indexes = personal_data.nothing_found_string
    context.bot.send_message(chat_id=update.effective_chat.id, text=our_indexes)

# ======= HELP FUNCTION =======
# TODO: Add the help function as it is required by Telegram Docs


# =========== OUR HANDLERS ==============
# Handlers are added in the same way they are written in the list of
# functions that is shown above

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button))

kyiv_index_handler = MessageHandler(Filters.text & (~Filters.command), search_for_index_in_mongo)
dispatcher.add_handler(kyiv_index_handler)

# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# dispatcher.add_handler(echo_handler)

updater.start_polling()
