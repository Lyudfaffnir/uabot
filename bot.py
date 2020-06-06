import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import personal_data
import find_index

updater = Updater(token=personal_data.token, use_context=True)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.start_string)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(update, context):
    request = update.message.text
    dict_indexes = find_index.get_table_on_page()
    answer = find_index.get_data_from_dictionary(dict_indexes, request)
    if answer == "":
        answer = personal_data.nothing_found_string
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()