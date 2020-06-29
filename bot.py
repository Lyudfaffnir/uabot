import logging
import personal_data
from mongodb import get_our_index
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler

# Global variables
city = ""

# Basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# ====== BOT START FUNCTION =====
# Should answer back with general specified information, such as "city" and "language"
# and the bot should set its settings depending on customer's answer. At the moment
# just response with the pre-generated text
# TODO: Set the dynamic inline kyeboard button
def start(update, context):
    keyboard = [[InlineKeyboardButton("Киев", callback_data="Kyiv")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.start_string, reply_markup=reply_markup)


def city(update, context):
    keyboard = [[InlineKeyboardButton("Киев", callback_data="Kyiv")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.choose_city_string,
                             reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()
    global city
    city = str(query.data)
    query.edit_message_text(text=personal_data.city_is_chosen)


# ====== DATABASE QUERY FUNCTION =========
# All the database-related functions can be found on the file mongodb.py. At the moment we have
# single collection with a single city, through which the query follows.
def search_for_index_in_mongo(update, context):
    user_input = update.message.text
    global city
    user_city = city
    reply_string = ""
    if user_city == "":
        reply_string = personal_data.city_has_not_been_chosen
    else:
        our_indexes = get_our_index(user_input, user_city)
        if our_indexes == {}:
            reply_string = personal_data.nothing_found_string
        else:
            reply_string += personal_data.bingo + f"Город: {city}\n"
            for count, (key, value) in enumerate(our_indexes.items(), 1):
                reply_string += "\n<i>" + str(key) + "</i>: <b>" + str(value) + "</b>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_string, parse_mode=ParseMode.HTML)


# ======= HELP FUNCTION =======
def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.help_string, parse_mode=ParseMode.HTML)


# =========== MAIN METHOD ==============
# Contains all the handlers and basic bot settings. Function is required by the official documents.
# Handlers are added in the same way they are written in the list of
# functions that is shown above
def main():
    updater = Updater(token=personal_data.token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    choose_city_handler = CommandHandler('city', city)
    dispatcher.add_handler(choose_city_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    search_index_handler = MessageHandler(Filters.text & (~Filters.command), search_for_index_in_mongo)
    dispatcher.add_handler(search_index_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
