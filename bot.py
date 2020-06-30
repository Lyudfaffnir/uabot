import logging
import personal_data
from mongodb import mongo_get_index, mongo_receive_cities
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
import emojis

# Global variables
current_city = ""
current_page = 1

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
    reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), 1))
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.start_string,
                             reply_markup=reply_markup)


# "/city" handler
def city_command(update, context):
    reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), 1))
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.choose_city_string,
                             reply_markup=reply_markup)


# inline query handler
# By default chooses the city
def button_command(update, context):
    query = update.callback_query
    query.answer()
    global current_page
    if str(query.data) == "page_back":
        if current_page <= 1:
            reply = f"Братан, ты и так на первой странице.{emojis.encode(':man_facepalming:')} " \
                    f"Мда, ну ты даёшь.{emojis.encode(':neutral_face:')}"
            reply += "\n" + personal_data.choose_city_string
        else:
            current_page -= 1
            reply = personal_data.choose_city_string
        reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), current_page))
        query.edit_message_text(text=reply, reply_markup=reply_markup)

    elif str(query.data) == "page_forward":
        current_page += 1
        reply_markup = InlineKeyboardMarkup(construct_cities_list(mongo_receive_cities(), current_page))
        query.edit_message_text(text=personal_data.choose_city_string, reply_markup=reply_markup)

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
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_string, parse_mode=ParseMode.HTML)


# "/help" handler
# Is a requirement of Telegram API
def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=personal_data.help_string,
                             parse_mode=ParseMode.HTML)


# "/find_city <user input>" handler
# TODO: Create search by city
def find_city_command(update, context):
    cities = mongo_receive_cities()
    if not context.args:
        text_reply = f'Не, кореш, ты не прошарил. Твоя команда должна выглядеть /find_city <i>твой запрос</i>.' \
                     f' Например, найти Киев\n /find_city Киев \nТеперь прошарил?'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_reply, parse_mode=ParseMode.HTML)
    else:
        _input = ''
        for word in context.args:
            _input += word
        reply_list = []
        for city in cities:
            if _input.upper() in city.upper():
                reply_list.append(city)
        if not reply_list:
            text_reply = f'Не, по такому запросу голяк. Посмотреть все города /city.'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text_reply, parse_mode=ParseMode.HTML)
        else:
            keyboard_reply = InlineKeyboardMarkup(construct_cities_list(reply_list, 1))
            text_reply = f"Вот, всё что накопал. {emojis.encode(':frowning:')} Только давай в темпе вальса."
            context.bot.send_message(chat_id=update.effective_chat.id, text=text_reply, reply_markup=keyboard_reply)


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
    dispatcher.add_handler(CallbackQueryHandler(button_command))
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
