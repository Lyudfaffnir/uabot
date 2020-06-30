import emojis

# /start command
txt_start = f"Привет{emojis.encode(':v:')}, пожалуйста выбери город."

# /help command
txt_help = f"Привет!{emojis.encode(':smiley:')} Этот бот поможет тебе найти индекс твоей улицы.\n" \
        f"{emojis.encode(':mag:')}Выбрать город - /city\n {emojis.encode(':see_no_evil:')}Разработчик: @lyudfaffnir"

txt_city_empty = f"Ну чувак, ты не выбрал город!{emojis.encode(':weary:')}. Попробуй ввести " \
              f"/city{emojis.encode(':anguished:')}"

# /city command
txt_available_cities = f"Сейчас доступны индексы для следующих городов:"

# button command
txt_zero_page = f"Братан, ты и так на первой странице.{emojis.encode(':man_facepalming:')} " \
             f"Мда, ну ты даёшь.{emojis.encode(':neutral_face:')}\n" + txt_available_cities
txt_no_reply = f'Не, по такому запросу голяк. Посмотреть все города /city.'
txt_cities_received = f"Вот, всё что накопал. {emojis.encode(':frowning:')} Только давай в темпе вальса."

# /find_city command
txt_no_input = f'Не, кореш, ты не прошарил. Твоя команда должна выглядеть /find_city <i>твой запрос</i>.\n' \
            f'Например, найти Киев\n /find_city Киев \nТеперь прошарил?'

# index handler
txt_city_found = f"Спасибо!{emojis.encode(':blush:')} Теперь просто пришли мне целое или часть названия улицы и я выдам " \
              f"всё что найду."
txt_index_not_found = f"Я не могу ничего найти по запросу {emojis.encode(':pensive:')}. Попробуй написать часть " \
                   f"названия улицы.\nВыбрать другой город - /city"
txt_bingo = f"{emojis.encode(':clap:')} Вуалля!\n"


def design_indexes(index_dict, city):
    txt_indexes = ''
    txt_indexes += txt_bingo + f"Город: {city}\n"
    for count, (key, value) in enumerate(index_dict.items(), 1):
        txt_indexes += f"\n<i>{str(key)}</i>: <b>{str(value)}</b>"
    return txt_indexes
