import logging
import personal_data
from mongodb import get_our_index
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

updater = Updater(token=personal_data.token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.start_string)


# ========= TEST ECHO FUNCTION ===========
#  Was ised to train echo_handler, does nothing at the moment, can be safely deleted

# def echo(update, context):
#    request = update.message.text
#    dict_indexes = find_index.get_table_on_page()
#    answer = find_index.get_data_from_dictionary(dict_indexes, request)
#    if answer == "":
#        answer = personal_data.nothing_found_string
#    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


def search_for_index_in_mongo(update, context):
    user_input = update.message.text
    our_indexes = get_our_index(user_input)
    if our_indexes == "":
        our_indexes = personal_data.nothing_found_string
    context.bot.send_message(chat_id=update.effective_chat.id, text=our_indexes)


# =========== OUR HANDLERS ==============
# Handlers are added in the same way they are written in the list of
# functions that is shown above
#
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

kyiv_index_handler = MessageHandler(Filters.text & (~Filters.command), search_for_index_in_mongo)
dispatcher.add_handler(kyiv_index_handler)

# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# dispatcher.add_handler(echo_handler)

updater.start_polling()