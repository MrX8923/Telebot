from datetime import datetime

import requests


API_KEY = 'e534bd70693e19e1bc08ccb611486a2e'
URLS = (
    'https://api.openweathermap.org/data/2.5/weather',
    'https://api.openweathermap.org/data/2.5/forecast'
)
CITY_ID = 498817


class No200CodeException(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return f"Не код 200! Получен: код {self.code}"


def make_request_for_weather(url: str, extra_headers: dict = None) -> dict | None:
    """
    Функция делает запрос, если не удалось, возвращает None
    :param url: адрес api
    :param extra_headers: доп. параметры запроса
    :return: словарь с данными или None
    """
    try:
        headers = {
            'apikey': API_KEY,
            'lang': 'ru',
            'units': 'metric',
            'id': CITY_ID
        }
        if extra_headers:
            headers.update(extra_headers)
        response: requests.Response = requests.get(url, headers)
        if response.status_code == 200:
            return response.json()
        raise No200CodeException(response.status_code)
    except No200CodeException as error:
        print(f'{error}')
    except Exception as error:
        print(error)


def weather_stripper(weather_day: dict, delta: bool = True) -> str:
    """
    Функция собирает текст для сообщения из словаря из запроса.
    :param weather_day: Словарь с данными за день
    :param delta: Флаг диапазона температуры
    :return: Строка сообщения
    """
    try:
        description: str = weather_day['weather'][0]['description']
        description = description[0].upper() + description[1:]
        temp: float = round(weather_day['main']['temp'], 1)
        feeling: float = round(weather_day['main']['feels_like'], 1)
        if delta:
            temp_min: float = round(weather_day['main']['temp_min'], 1)
            temp_max: float = round(weather_day['main']['temp_max'], 1)
            date_temp_delta = f"Диапазон: {temp_min}°C ... {temp_max}°C\n"
        else:
            date_temp_delta = ''
        wind_speed: float = round(weather_day['wind']['speed'], 1)
        date = datetime.utcfromtimestamp(weather_day['dt']).strftime("%d.%m.%y")
        return f"{date}: {description}\n" \
               f"Температура: {temp}°C\n" \
               f"{date_temp_delta}" \
               f"Ощущается как: {feeling}°C\n" \
               f"Скорость ветра: {wind_speed} м/с\n"
    except (KeyError, ValueError, IndexError, TypeError):
        return "Похоже изменилась схема json c данными.\n" \
               "Обратитесь к разработчику."


def make_weather_message(ind: int = 0) -> str:
    """
    В зависимости от переданного параметра функция формирует сообщение для бота о погоде.
    :param ind: 0 - на 1 день, 1 - на 5 дней
    :return: Строковое сообщение
    """
    if not ind:
        weather_now = make_request_for_weather(URLS[0])
        if weather_now:
            message = weather_stripper(weather_now)
            return message
    else:
        weather_forecast = make_request_for_weather(URLS[1])['list']
        if weather_forecast:
            temp = []
            for day in weather_forecast:
                if '12:00:00' in day['dt_txt']:
                    temp.append(weather_stripper(day, delta=False))
            message = '\n'.join(temp)
            return message
    return "Что-то пошло не так, попробуйте позже..."
