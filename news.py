from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def send_news() -> str:
    """
    Функция парсит страничку Фонтанки и возвращает главные новости с нее.
    :return: Сообщение для отправки ботом.
    """
    print('*Начало.')
    print('*Запускаем браузер FireFox в фоновом режиме.')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print('*Браузер открыт в фоновом режиме.')
    WebDriverWait(driver, 5)
    print('*Открываем сайт "Фонтанка"')
    driver.get('https://www.fontanka.ru/24hours.html')
    WebDriverWait(driver, 10)\
        .until(lambda x: x.find_elements(By.CLASS_NAME, 'H7b1'))
    print('*Собираем самые важные новости.')
    news_list = driver.find_elements(By.CLASS_NAME, 'H7b1')
    temp = "\n\n".join([i.text for i in news_list if news_list.index(i) < 7])
    print(*temp)
    driver.quit()
    return f'Фонтанка.ру\n' \
           f'КАРТИНА ДНЯ\n\n' \
           f'{temp}'
