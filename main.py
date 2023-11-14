import telebot

import weather_json
import anekdot
import movie
import news

from random import choice

TOKEN = '6212594744:AAHGswqaPzPw-dvf4JVBypW_rc20l-TKDAY'

BOT = telebot.TeleBot(TOKEN)


@BOT.message_handler(content_types=['text'])
def message(info):
    """
    Функция бота Телеграм обрабатывает запросы пользователя,
    запускает функции в соответствии с запросами.
    :param info: Объект с сообщением пользователя.
    """
    if 'погода5' in info.text.lower():
        BOT.send_message(info.chat.id, weather_json.make_weather_message(ind=1))
    elif 'погода' in info.text.lower():
        BOT.send_message(info.chat.id, weather_json.make_weather_message())
    elif 'анекдот' in info.text.lower():
        BOT.send_message(info.chat.id, anekdot.send_anekdot())
    elif 'кино' in info.text.lower():
        BOT.send_message(info.chat.id, 'Выберите, что посоветовать:\n'
                                       '1. Комедия.\n'
                                       '2. Хорор.\n'
                                       '3. Боевик. \n'
                                       '4. Фантастика.\n'
                                       '5. Вестерн.')
    elif 'комедия' in info.text.lower() \
            or 'хорор' in info.text.lower() \
            or 'боевик' in info.text.lower() \
            or 'фантастика' in info.text.lower() \
            or 'вестерн' in info.text.lower():
        BOT.send_message(info.chat.id,
                         movie.send_movie_recommendation(info.text.lower()))
    elif 'фильм' in info.text.lower():
        BOT.send_message(info.chat.id,
                         movie.send_movie_recommendation(info.text.lower()
                                                         .replace('фильм ', '')))
    elif 'новости' in info.text.lower():
        BOT.send_message(info.chat.id, news.send_news())
    else:
        BOT.send_message(info.chat.id, choice(['Бот здесь!', 'Присматриваю!', 'Вижу всё!']))


if __name__ == '__main__':
    BOT.infinity_polling(none_stop=True)
