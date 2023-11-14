from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from random import choice


def make_movie_message_genre(driver, genre: str) -> str:
    """
    Функция парсит страничку сайта и собирает сообщение для отправки.
    Возвращает строку - готовое сообщение для отправки ботом.
    :param driver: Браузер.
    :param genre: Жанр фильма.
    :return: Сообщение для отправки.
    """
    print(f'Берем случайный фильм по жанру: {genre}.')
    WebDriverWait(driver, 90) \
        .until(lambda x: x.find_elements(By.CLASS_NAME, 'loadlate'))
    choice(driver.find_elements(By.CLASS_NAME, 'loadlate')).click()
    WebDriverWait(driver, 30) \
        .until(lambda x: x.find_element(By.CLASS_NAME, 'sc-466bb6c-3'))
    return f'{driver.find_element(By.TAG_NAME, "h1").text}\n' \
           f'{driver.find_element(By.CLASS_NAME, "sc-bde20123-1").text}\n' \
           f'{driver.find_element(By.CLASS_NAME, "sc-466bb6c-3").text}\n'


def random_search(driver, query: str) -> str:
    """
    Функция по случайному запросу пользователя пытается найти фильм.
    Возвращает строку с названием, рейтингом и кратким описанием.
    :param driver: Браузер.
    :param query: Запрос пользователя.
    :return: Сообщение бота.
    """
    driver.get('https://www.imdb.com')
    WebDriverWait(driver, 5)
    print(f'Ищем: {query}')
    driver.find_element(By.ID, 'suggestion-search').send_keys(query)
    driver.find_element(By.ID, 'suggestion-search-button').click()
    WebDriverWait(driver, 10) \
        .until(lambda x: x.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__tc'))
    choice(driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__tc')).click()
    WebDriverWait(driver, 10) \
        .until(lambda x: x.find_element(By.CLASS_NAME, 'sc-466bb6c-3'))
    print('Собираем ответ на поисковый запрос.')
    return f'{driver.find_element(By.TAG_NAME, "h1").text}\n' \
           f'{driver.find_element(By.CLASS_NAME, "sc-bde20123-1").text}\n' \
           f'{driver.find_element(By.CLASS_NAME, "sc-466bb6c-3").text}\n'


def send_movie_recommendation(genre: str) -> str:
    """
    Функция парсит сайт imdb, находит фильм по жанру, указанному пользователем.
    Возвращает строку с названием, рейтингом и кратким описанием.
    :param genre: Запрос пользователя.
    :return: Сообщение бота для пересылки.
    """
    print('*Начало.')
    genre = genre[1:]
    print(f'{genre = }')
    print('*Запускаем браузер FireFox в фоновом режиме.')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print('*Браузер открыт в фоновом режиме.')
    WebDriverWait(driver, 5)
    print('*Открываем сайт IMDB.')
    match genre:
        case 'комедия':
            driver.get('https://www.imdb.com/search/title/?genres=Comedy&sort=user_rating,'
                       'desc&title_type=feature&num_votes=25000,&ref_=chttp_gnr_4')
            message = make_movie_message_genre(driver, genre)
        case 'хорор':
            driver.get('https://www.imdb.com/search/title/?genres=Horror&sort=user_rating,'
                       'desc&title_type=feature&num_votes=25000,&ref_=chttp_gnr_12')
            message = make_movie_message_genre(driver, genre)
        case 'боевик':
            driver.get('https://www.imdb.com/search/title/?genres=Action&sort=user_rating,'
                       'desc&title_type=feature&num_votes=25000,&ref_=chttp_gnr_0')
            message = make_movie_message_genre(driver, genre)
        case 'фантастика':
            driver.get('https://www.imdb.com/search/title/?genres=Sci-Fi&sort=user_rating,'
                       'desc&title_type=feature&num_votes=25000,&ref_=chttp_gnr_17')
            message = make_movie_message_genre(driver, genre)
        case 'вестерн':
            driver.get('https://www.imdb.com/search/title/?genres=Western&sort=user_rating,'
                       'desc&title_type=feature&num_votes=25000,&ref_=chttp_gnr_22')
            message = make_movie_message_genre(driver, genre)
        case _:
            message = random_search(driver, genre)
    print(message)
    # driver.quit()
    return message
