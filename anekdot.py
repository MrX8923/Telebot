from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from random import choice


def send_anekdot():
    print('*Начало.')
    print('*Запускаем браузер FireFox в фоновом режиме.')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print('*Браузер открыт в фоновом режиме.')
    WebDriverWait(driver, 2)
    print('*Открываем сайт Anekdot.ru.')
    driver.get('https://www.anekdot.ru/last/anekdot/')
    WebDriverWait(driver, 2)
    print('*Загружаем анекдот.')
    WebDriverWait(driver, 2)
    print()
    message = choice(driver.find_elements(By.CLASS_NAME, 'text')) \
        .text \
        .replace('. ', '.\n') \
        .replace('? ', '?\n') \
        .replace('! ', '!\n') \
        .replace(': ', ':\n')
    print(message)
    print()
    print('*Отправляем в телеграм')
    driver.quit()
    return message
