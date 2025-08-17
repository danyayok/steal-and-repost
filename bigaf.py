import re
import json
import time
import pickle
import base64
import random
import requests
import telebot
import collections
import g4f.Provider
from PIL import Image
from io import BytesIO
from telebot import types
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from g4f.client import Client as G4FClient
from g4f import models
from bs4 import BeautifulSoup


#
# Куча функций
#

def post_x(message, usrname):
    driver.get("https://x.com/home")
    print("Начало постинга в твиттер")
    time.sleep(10)
    input_text = driver.find_element(By.XPATH, "*//*[@contenteditable='true']")
    input_text.send_keys(message)
    btn = driver.find_element(By.XPATH, "*//*[@data-testid='tweetButtonInline']")
    btn.click()
    print("Отправка поста")
    time.sleep(5)
    driver.get(f"https://x.com/{usrname}")
    time.sleep(5)
    post = driver.find_element(By.XPATH,
                               '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div[1]/div/article')
    post.click()
    time.sleep(5)
    driver.save_screenshot("post_x.png")
    return driver.current_url


def login_x(email, password, usrname):
    try:
        driver.get("https://x.com/home/")
        load_cookies(driver, 'cookies_x.pkl')
        driver.refresh()  # Обновляем страницу, чтобы куки применились
        print("Куки загружены, вы уже вошли в систему.")
        time.sleep(8)
    except FileNotFoundError:
        driver.get('https://x.com/i/flow/login')
        print("Куки не найдены, выполняем вход.")
        print("Заход на х.сом")
        time.sleep(5)
        print("Ввод почты")
        input_email = driver.find_element(By.NAME, "text")
        input_email.send_keys(email)
        input_email.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            if driver.find_element(By.XPATH, "//span[text()='Enter your phone number or username']"):
                print("Ввод имени пользователя")
                input_name = driver.find_element(By.NAME, "text")
                input_name.send_keys(usrname)
                input_name.send_keys(Keys.ENTER)
                time.sleep(3)
        except Exception as e:
            print("не надо ник вводить")
        print("Ввод пароля")
        input_password = driver.find_element(By.NAME, "password")
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            if driver.find_element(By.XPATH, "//span[text()='Check your email' and @name='name']"):
                print("Запрос почты")
                # Вводим код на сайте
                input_code = driver.find_element(By.NAME, "text")
                code = input("Введите код с почты: ")
                input_code.send_keys(code)
                input_code.send_keys(Keys.ENTER)
                time.sleep(5)
        except Exception as e:
            print("Нет необходимости в коде с почты:", e)
            time.sleep(5)
        save_cookies(driver, 'cookies_x.pkl')


# Инста ещё не сделана для бота полностью
def login_inst(email, password):
    try:
        driver.get("https://www.instagram.com/")
        time.sleep(5)
        load_cookies(driver, "cookies_inst.pkl")
        print("Куки загружены, вы уже вошли в систему.")
        driver.refresh()
    except:
        print("Куки не найдены, выполняем вход.")
        driver.get("https://www.instagram.com/")
        time.sleep(10)
        input_email = driver.find_element(By.XPATH, "//input[@aria-label='Phone number, username, or email']")
        input_email.send_keys(email)
        input_pass = driver.find_element(By.XPATH, "//input[@aria-label='Password' and @type='password']")
        input_pass.send_keys(password)
        input_pass.send_keys(Keys.RETURN)
        time.sleep(15)
        try:
            # Если инста запрашивает код с почты/телефона то проходит сюда
            input_code = driver.find_element(By.ID, ":r7:")
            code = input("Введите код для Инстаграмма: ")
            input_code.send_keys(code)
            input_code.send_keys(Keys.RETURN)
            time.sleep(10)
        except:
            print("Код не нужен")
        time.sleep(20)


def post_inst(message, usrname, file_path):
    driver.get("https://www.instagram.com/")
    load_cookies(driver, "cookies_inst.pkl")
    driver.refresh()
    time.sleep(5)
    # Проверяем, выполнен ли вход
    if "login" in driver.current_url:
        raise Exception("Не выполнен вход в аккаунт Instagram")
    # Нажимаем на кнопку "Создать пост"
    post_button = WebDriverWait(driver, 200).until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@class='x1n2onr6'])[9]")))
    time.sleep(random.uniform(1, 5))
    post_button.click()
    # Загружаем изображение
    file_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._ac69")))
    time.sleep(random.uniform(1, 5))
    file_input.send_keys(file_path)
    print(1)
    # Переходим к следующему шагу
    # next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.xjyslct")))
    time.sleep(10)
    driver.save_screenshot("picture.png")
    next_button = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.xjyslct")))
    time.sleep(random.uniform(1, 5))
    next_button.click()
    time.sleep(10)
    driver.save_screenshot("next.png")
    print(2)
    # Нажимаем "Next" второй раз
    next_button = WebDriverWait(driver, 200).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".xyamay9 > div:nth-child(1)")))
    time.sleep(random.uniform(1, 5))
    next_button.click()
    driver.save_screenshot("next2.png")
    print(3)
    # Вводим текст
    text_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Write a caption...')]")))
    time.sleep(random.uniform(1, 5))
    for char in message:
        text_input.send_keys(char)
        time.sleep(0.05)
    driver.save_screenshot("text.png")
    print(4)
    # Публикуем пост
    share_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Share' and @role='button']")))
    share_btn.click()
    time.sleep(10)
    driver.save_screenshot("posted.png")
    print("Пост успешно опубликован!")
    # получаем ссылку на пост
    driver.get(f"https://www.instagram.com/{usrname}/")
    time.sleep(5)
    post = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div._ac7v:nth-child(1) > div:nth-child(1) > a:nth-child(1)")))
    post.click()
    time.sleep(3)
    return driver.current_url


# def post_inst(message):
#   # Path to the image file
#   file_path = r"/content/map.png"
#   # Initialize the WebDriver
#   driver.get("https://www.instagram.com/")
#   time.sleep(5)
#   # Assuming you're already logged in
#   # Locate and click the "Create Post" button
#   post_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "(//div[@class='x1n2onr6'])[9]"))
#   )
#   post_button.click()
#   # Wait for the file input to appear
#   file_input = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
#   )
#   # Send the file path to the input
#   file_input.send_keys(file_path)
#   # Всё выше (до начала функции) код со stackoverflow
#   time.sleep(5)
#   driver.save_screenshot("picture.png")
#   # переменные next нажимаются для перехода к написанию текста, минуя возможность добавить фильтры на фото
#   next = driver.find_element(By.XPATH, "//div[text()='Next' and @role='button']")
#   next.click()
#   time.sleep(3)
#   driver.save_screenshot("next.png")
#   # next2 = driver.find_element(By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(text(), 'Next') and @role='button']")
#   next.click()
#   time.sleep(3)
#   driver.save_screenshot("next2.png")
#   text_input = driver.find_element(By.XPATH, "//div[contains(@class, 'xw2csxc') and @aria-label='Write a caption...' and @role='textbox']")
#   # в соцсетях цукерберка не выходит всё сообщение сразу кинуть, надо по символу
#   for char in message:
#     text_input.send_keys(char)
#   driver.save_screenshot("text.png")
#   share_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(text(), 'Share') and @role='button']")
#   share_btn.click()
#   time.sleep(3)
#   save_cookies(driver, "cookies_inst.pkl")


def login_fb(email, password):
    try:
        driver.get("https://www.facebook.com/")
        time.sleep(8)
        print("cookies")
        load_cookies(driver, "cookies_fb.pkl")
        driver.refresh()  # Обновляем страницу, чтобы применить куки
    except FileNotFoundError:
        driver.get("https://www.facebook.com/login/")
        time.sleep(7)
        input_email = driver.find_element(By.XPATH, "//input[@placeholder='Email address or phone number']")
        input_email.send_keys(email)
        input_pass = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        input_pass.send_keys(password)
        button = driver.find_element(By.ID, "loginbutton")
        button.click()
        time.sleep(30)
        save_cookies(driver, "cookies_fb.pkl")


def post_fb(message):
    driver.get("https://www.facebook.com/")
    time.sleep(50)
    mind = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1ejq31n:nth-child(3)")))
    mind.click()
    text_area = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".xmper1u > div:nth-child(1)")))
    for char in message:
        text_area.send_keys(char)
        time.sleep(0.1)
    driver.save_screenshot("writed.png")
    # Кликаем на кнопку "Опубликовать"
    post_button = WebDriverWait(driver, 200).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Опубликовать']")))
    post_button.click()
    time.sleep(5)
    driver.save_screenshot("sended.png")
    driver.get("https://www.facebook.com/profile.php?id=61571046076103")
    link = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH,
                                                                        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/div/span[1]/span/span/a")))
    link.click()
    return driver.current_url


def login_site(email, password):
    try:
        driver.get("https://app.from.biz/login/")
        time.sleep(5)
        load_cookies(driver, "cookies_from.pkl")
        print("Куки загружены, вы уже вошли в систему.")
        driver.refresh()
    except:
        print("Куки не найдены, выполняем вход.")
        driver.get("https://app.from.biz/login/")
        input_email = driver.find_element(By.NAME, "email")
        input_pass = driver.find_element(By.NAME, "password")
        time.sleep(3)
        for char in password:
            input_pass.send_keys(char)
        for char in email:
            input_email.send_keys(char)
        btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        driver.save_screenshot("login.png")
        btn.click()
        time.sleep(5)
        driver.save_screenshot("login1.png")
        save_cookies(driver, "cookies_from.pkl")


def post_site(message):
    print(message)
    driver.get("https://app.from.biz/saity/311737/pages/")
    # Ожидание загрузки страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Страница сайта")
    # Ожидание кнопки и клик
    btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn:nth-child(5)')))
    btn.click()
    print("Кнопка мат-ы")
    # Ожидание поля ввода заголовка
    time.sleep(5)
    add_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-3:nth-child(2) > a:nth-child(1)")))
    add_btn.click()
    title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "title_1")))
    title.send_keys(message["title"])
    print("Заголовок")
    time.sleep(2)
    driver.save_screenshot("d.png")
    # Ожидание выпадающего списка и выбор
    pg_choose = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                            '/html/body/div[16]/div/div/div[2]/form/div[1]/div/div/div/div[1]/div/div/div[2]/fieldset/div/div/div/button')))
    print("WEB")
    pg_choose.click()
    print("click")
    news_choose = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bs-select-4-9"]')))
    print("choose")
    news_choose.click()
    print("Список с типом новости (вроде)")
    time.sleep(2)
    # Ожидание поля даты
    date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='field_786_MzExNzQw_311741']")))
    date.clear()
    date.send_keys(message["date"])
    print("Ввод даты")
    time.sleep(2)
    # Ожидание раскрытия секции описания
    btn = driver.find_element(By.XPATH, '//*[@id="heading_cecdd096144eccaeb28c4c2bc233ed63"]/button')
    # btn.click() # Нажимаем на кнопку "Материалы" что бы перейти ниже
    # time.sleep(3)
    driver.save_screenshot("d1.png")
    desc_fast = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_4425"]')))
    desc_fast.send_keys(message["desc"] if message["desc"] else gpt(
        "Сделай краткое описание этого текста. Твой ответ максимум 2 предложения. Текст: ", message["desc"]))
    # Ожидание поля краткого описания и ввод данных
    print("Быстрое описание")
    desc_full = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                     "//div[contains(@class, 'ck-content') and contains(@class, 'ck-editor__editable') and @lang='ru' and @role='textbox' and @aria-label='Область редактирования редактора: main']")))
    for char in " " + message['desc']:
        desc_full[0].send_keys(char)
    print("Ввод описания полного")
    # Вставка фото
    driver.save_screenshot("d2.png")

    try:
        if message['img_link']:
            img_main = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#link_8d255d90e10ab51c195e7372f02dce03')))
            img_main.send_keys(message["img_link"])
            main_con = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#field_8d255d90e10ab51c195e7372f02dce03 > div:nth-child(1) > button:nth-child(3)')))
            main_con.click()
            time.sleep(5)
            add_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="heading_065a4bdc2e5a9f1a6e51aeabcf1b4e4e"]/button')))
            add_btn.click()
            time.sleep(5)
            img_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="link_9814b048a08d099ae91420c48aa2221a"]')))
            img_input.send_keys(message["img_link"])
            print("img_link")
            img_con = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#field_9814b048a08d099ae91420c48aa2221a > div:nth-child(1) > button:nth-child(3)')))
            img_con.click()
            driver.save_screenshot("d3.png")
    except Exception as e:
        print(e)
        print("Нету фото (ссылки на фото)")
    # Подтверждение сохранения
    # if input("Если хотите отправить новость, напишите 'Отправить': ") == "Отправить":
    time.sleep(5)
    btn_save = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-save"]')))
    btn_save.click()
    time.sleep(5)
    driver.save_screenshot("d3.png")


# Загрузка куки

def load_cookies(driver, path):
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def gpt(prompt, text):
    client = G4FClient()
    for i in range(10):
        print("Запрос чату гпт ", i + 1)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": prompt + text}],
        )
        res = response.choices[0].message.content

        if len(res) > 0 and 'Model' not in res and 'error' not in res and 'chat' not in res and "discord" not in res:
            print("Ответ GPT получен!")
            return res
            break


def get_answer(text):
    client = G4FClient()
    for i in range(10):
        print("Запрос чату гпт ", i + 1)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": text}],
        )
        res = response.choices[0].message.content
        print(res)
        if len(res) > 0 and 'Model' not in res and 'error' not in res and 'chat' not in res and res.split(",")[
            0].isdigit():
            print("Ответ GPT получен!")
            return res.split(",")


def describe(text):
    client = G4FClient()
    for i in range(10):
        print("Запрос чату гпт ", i + 1)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user",
                       "content": "Перескажи этот текст, текст который ты отправил должен быть не больше 4х предложений, если текст не предоставлен, то отправь просто пробел, ничего более: " + text}],
        )
        res = response.choices[0].message.content

        if len(res) > 0 and 'Model' not in res and 'error' not in res and 'chat' not in res and "discord" not in res and "exceed" not in res:
            print("Ответ GPT получен!")
            return res
            break


def rework_mark(text):
    replacements = {
        '@': r'\@',
        '/': r'\/',
        '#': r'\#',
        ':': r'\:',
        '_': r'\_',
        '*': r'\*',
        '~': r'\~',
        '.': r'\.',
        '|': r'\|',
        '-': r'\-',
        '!': r'\!',
        '(': r'\(',
        ')': r'\)',
        '=': r'\=',
        '+': r'\+',
    }

    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)

    return text


def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")


# https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,offline&response_type=token&v=5.199
# вот сюда заходишь и токен пользователя для права на публикацию постов получаешь
# id приложухи - 52649878, его надо вставить заместо YOUR_APP_ID
# def vk_photo_upload()
def vk_posting(message, img_link):
    version = '5.131'
    access_token = 'vk1.a.S_ryDM_T1VtxGbblx-PieokkP2fYFotBmFjidFYNkIhThNvYONG6vmrTjMm5h5GBzP0i3q9mJxk2oVvt4IIstINbIQD_vxM-J1MaCt5w2hBwgf8BVuP_kaAy5KNLzEcs3oH9U_A3pMuTevAUxKZtNSZ8UYTWovIrk16ooFaxUv1_IkZ3nAqwfpKkdCqgHSgXFoYlpa7BbZrTeS_wrsgrFQ'
    pablik_id = -228793052
    url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": access_token,
        "v": "5.131",
        "owner_id": pablik_id,
        "message": message,
        # "attachments": img_link,
        "from_group": 1,
    }

    # Отправка запроса
    response = requests.post(url, params=params)
    # Обработка ответа
    data = response.json()
    if "response" in data:
        print(f"Пост опубликован! ID поста: {data['response']['post_id']}")
        return f"vk.ru/wall{pablik_id}_{data['response']['post_id']}"
    else:
        print(f"Ошибка: {data.get('error', 'Неизвестная ошибка')}")


#
# вот это ниже это код михаила
#

def search_photo(ACCESS_KEY, search_tags):
    headers_post = {"Authorization": f"Client-ID {ACCESS_KEY}"}
    DOMAIN_UNSPLASH = 'https://api.unsplash.com'

    image_urls = []

    for search_tag in search_tags:
        if search_tag:
            params = {
                'page': 1,
                'query': search_tag,
                'orientation': 'landscape',
                'per_page': 10
            }
            url = f'{DOMAIN_UNSPLASH}/search/photos'

            print(f'Ищем фотографии по тегам...')
            response = requests.get(url, headers=headers_post, params=params)

            for i in range(0, 2):
                random_number = random.randint(0, 9)
                if response.json()['results'][random_number]['urls'].get('full'):
                    image_urls.append(response.json()['results'][random_number]['urls']['full'])

    if len(image_urls) != 0:
        print(f'В выборку добавлено {len(image_urls)} изображений')
    else:
        print('Фотографии не найдены. Возвращаем заглушку')
        params = {
            'page': 1,
            'query': 'office',
            'orientation': 'landscape',
            'per_page': 10
        }
        response = requests.get(url, headers=headers_post, params=params)
        for i in range(0, 6):
            random_number = random.randint(0, 9)
            if response.json()['results'][random_number]['urls'].get('full'):
                image_urls.append(response.json()['results'][random_number]['urls']['full'])

        print('Заглушка найдена')
    if len(image_urls) != 0:
        return image_urls
    else:
        return None


def make_tags(text: str) -> list:
    prompt = 'Напиши о чём этот текст ТОЛЬКО одним ключевым словом на английском языке для поиска картинки для иллюстрации. Не используй фамилии. Сделай это два раза. Раздели эти два слова запятой. Кроме двух слов ничего не возвращай: \n'
    model = models.gpt_4o
    i = 0
    loops = 12
    while i < loops:
        client = G4FClient()  # экземпляр класса
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f'{prompt}'
                },
                {
                    "role": "user",
                    "content": f'{text}'
                },
            ]
        )
        print('Выбрана модель ', model)
        res = response.choices[0].message.content

        res = re.sub(r"[А-Яа-яЁё]", "", res)

        comma_count = res.count(',')

        phrases = [phrase.strip() for phrase in res.split(',')]

        if (comma_count == 1) and (len(phrases) == 2) and (len(phrases[-1]) > 0):
            print('Созданы ключевые слова \n')
            return phrases
        else:
            i += 1
            print('Сделать ключевые слова не удалось. Попытка №', i, 'из ', loops, '...')
    return None


def choose_best_image(image_urls, text):
    client = G4FClient(provider=g4f.Provider.Blackbox)

    print('Преобразуем выбранные изображения в машиночитаемый вид')
    images = []
    for url in image_urls:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            images.append([image, url.split("/")[-1]])  # Добавление имени файла из URL

    i = 0
    loops = 15

    while i < loops:
        prompt = f"Какое из этих изображений больше подходит для текста? В ответе дай ТОЛЬКО номер и ничего больше. Текст {text}"
        print('Выбор наиболее оптимального изображения')
        response = client.chat.completions.create([{"content": prompt, "role": "user"}], "", images=images)

        # Вывод результата
        result = response.choices[0].message.content
        last_word = result.split()[-1] if result.split() else None

        if last_word is not None and last_word.isdigit() and len(image_urls) >= int(
                last_word):  # Проверяем, что это число
            print('Наиболее оптимальное изображение найдено')
            print(image_urls)
            print(last_word)
            return image_urls[int(last_word)]
        else:
            i += 1
            print('Найти наилучшее изображение пока не удалось. Попытка №', i + 1, 'из ', loops, '...')

    print('Найти наилучшее изображение пока не удалось')
    return None


#
# ПАРСИНГ, ВСЕ САЙТЫ ПО ТЗ
#

def fetch_news_from_sources(sources, parse_function):
    """
    Обрабатывает список источников с помощью переданной функции парсинга.
    """
    all_news = []
    for source in sources:
        response = requests.get(source)
        soup = BeautifulSoup(response.text, "html.parser")
        all_news.extend(parse_function(soup))
    return all_news


def parse_commersant(soup):
    """Парсинг новостей с сайта Коммерсантъ."""
    news_list = []
    news_items = soup.find_all('article', class_="uho rubric_lenta__item js-article")
    for item in news_items:
        link = item.get("data-article-url", "")
        response = requests.get(link)
        soup1 = BeautifulSoup(response.text)
        desc = soup1.find('div', class_='doc__body').get_text(strip=True) if link[26: 29] == "doc" and soup1.find('div',
                                                                                                                  class_='doc__body') else soup1.find(
            'div', class_='doc__text doc__intro js-search-mark').get_text(strip=True)
        news_list.append({
            "title": item.get("data-article-title", ""),
            "desc": desc,
            "date": item.find('p', class_="uho__tag rubric_lenta__item_tag hide_mobile").get_text(strip=True),
            "link": link,
            "src": "Коммерсантъ"
        })
    return news_list


def parse_rbk(soup):
    """Парсинг новостей с сайта РБК."""
    news_list = []
    news_items = soup.find_all('div', class_="item__wrap l-col-center")
    for item in news_items:
        link = item.find("a", class_="item__link rm-cm-item-link js-rm-central-column-item-link")
        link_url = link.get("href", "")
        response = requests.get(link_url)
        sub_soup = BeautifulSoup(response.text, "html.parser")
        content = sub_soup.find("div", class_="article__text article__text_free")
        news_list.append({
            "title": item.find("span", class_="normal-wrap").get_text(strip=True),
            "desc": content.get_text(strip=True) if content else "",
            "date": item.find("span", class_="item__category").get_text(strip=True),
            "link": link_url,
            "src": "РБК"
        })
    return news_list


def parse_pravo(soup):
    """Парсинг новостей с сайта Право.ru."""
    news_list = []
    news_items = soup.find_all('div', class_="search-results__item")
    for item in news_items:
        news_list.append({
            "title": item.find("header", class_="block_header").get_text(strip=True),
            "desc": item.find("article").get_text(strip=True),
            "date": item.find("div", class_="date muted").get_text(strip=True),
            "link": item.find("a")["href"],
            "src": "Право.ru"
        })
    return news_list


def parse_fpa(soup):
    """Парсинг новостей с сайта Федеральной Палаты Адвокатов."""
    news_list = []
    news_item = soup.find_all('div', class_="news-item news-item--v2")
    news_item2 = soup.find_all('div', class_="news-item news-item--v2 news-item--no-photo news-item--border")
    news_item3 = soup.find_all('div', class_="news-item news-item--v2 news-item--white")
    for j in news_item:
        desc_div = j.find("div", class_="news-item__text")
        date_div = j.find("div", class_="news-item__date")
        if "t.me" not in j.find("a")["href"]:
            news_list.append({
                "title": j.find("a").get_text(strip=True).replace("\xa0", ""),
                "desc": desc_div.get_text(strip=True).replace("\xa0", "") if desc_div else "",
                "date": date_div.get_text(strip=True).replace("\xa0", "") if date_div else "",
                "link": "https://fparf.ru" + j.find("a")["href"],
                "src": "Федеральная Палата Адвокатов"
            })
    for j in news_item2:
        title = j.find("a").get_text(strip=True).replace("\xa0", "")
        desc_div = j.find("div", class_="news-item__text")
        date_div = j.find("div", class_="news-item__date")
        if "t.me" not in j.find("a")["href"]:
            news_all.append({
                "title": title,
                "desc": desc_div.get_text(strip=True).replace("\xa0", "") if desc_div else "",
                "date": date_div.get_text(strip=True).replace("\xa0", "") if date_div else "",
                "link": "https://fparf.ru" + j.find("a")["href"],
                "src": "Федеральная Палата Адвокатов"
            })

    for j in news_item3:
        title = j.find("a").get_text(strip=True).replace("\xa0", "")
        desc_div = j.find("div", class_="news-item__text")
        date_div = j.find("div", class_="news-item__date")
        if "t.me" not in j.find("a")["href"]:
            news_all.append({
                "title": title,
                "desc": desc_div.get_text(strip=True).replace("\xa0", "") if desc_div else "",
                "date": date_div.get_text(strip=True).replace("\xa0", "") if date_div else "",
                "link": "https://fparf.ru" + j.find("a")["href"],
                "src": "Федеральная Палата Адвокатов"
            })

    return news_list


# def fetch_news_mvd(news_all, pages=10):
#     for page in range(pages):
#         response = requests.get(f"https://xn--b1aew.xn--p1ai/news/{page}")
#         soup = BeautifulSoup(response.text, "html.parser")
#         news = soup.find_all('div', class_="sl-item")
#         print("MVD is filling...")
#         for i in news:
#             news_all.append({
#                 "title": i.find("a").get_text(strip=True),
#                 "desc": i.find("div", class_="sl-item-text").get_text(strip=True).replace("\xa0", ""),
#                 "date": i.find("div", class_="sl-item-date").get_text(strip=True),
#                 "link": i.find("a")["href"],
#                 "src": "МВД"
#             })

# def fetch_news_sledcom(news_all):
#     response = requests.get('https://sledcom.ru/news')
#     soup = BeautifulSoup(response.text, "html.parser")
#     news = soup.find_all('div', class_="inner-page__list-item ")
#     print("Sledcom is filling...")
#     for j in news:
#         up = j.find("div", class_="news-item__title")
#         down = j.find("div", class_="news-item__footer")
#         response = requests.get(up.find("a")["href"])
#         soup = BeautifulSoup(response.text, "html.parser")
#         desc = soup.find('div', class_="news-card__text")
#         news_all.append({
#             "title": up.find("a").get_text(strip=True),
#             "desc": desc.get_text(strip=True) if desc else "",
#             "date": down.find("div", class_="news-item__data").get_text(strip=True) + " " + up.find("div", class_="news-item__time").get_text(strip=True),
#             "link": up.find("a")["href"],
#             "src": "Следком"
#         })

# def fetch_news_supreme_court(news_all, urls):
#     for url in urls:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         news = soup.find_all('div', class_="clearfix")
#         for j in news:
#             title = j.find("a").get_text(strip=True).replace("\xa0", "")
#             desc_div = j.find("div", class_="vs-list-item vs-grid-large")
#             date_div = j.find("div", class_="vs-grid-tiny")

#             news_all.append({
#                 "title": title,
#                 "desc": desc_div.find("a").get_text(strip=True).replace("\xa0", "") if desc_div else "",
#                 "date": date_div.get_text(strip=True) if date_div else "",
#                 "link": desc_div.find("a")["href"] if desc_div else "",
#                 "src": "Верховный Суд РФ"
#             })

# Источники
commersant = ['https://www.kommersant.ru/rubric/3?from=burger', 'https://www.kommersant.ru/rubric/2?from=burger',
              'https://www.kommersant.ru/rubric/6?from=burger']
erbeka = ['https://rostov.rbc.ru/rostov/']
pravo = ['https://pravo.ru/news/']
fpa = [f"https://fparf.ru/news/?PAGEN_1={i}" for i in range(5)]

# Сбор новостей
news_all = []
news_all.extend(fetch_news_from_sources(commersant, parse_commersant))
news_all.extend(fetch_news_from_sources(erbeka, parse_rbk))
news_all.extend(fetch_news_from_sources(pravo, parse_pravo))
news_all.extend(fetch_news_from_sources(fpa, parse_fpa))
for i in news_all:
    print(i["src"], i["link"], i["title"], "КОНЕЦ TITLE НАЧАЛО DESC", i["desc"])
# Форматирование итогового результата
news_botu = "\n".join(
    f"{idx} {news['title'] if news['title'] else news['desc']} {news['src']}" for idx, news in enumerate(news_all))
print(news_botu)


def vk_posting(message, owner_id, media_id):
    attach = f"photo{owner_id}_{media_id}"
    version = '5.199'
    access_token = 'nuh uh'
    pablik_id = 'nuh uh'
    url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": access_token,
        "v": version,
        "owner_id": pablik_id,
        "message": message,
        "attachments": attach,
        "from_group": 1,
    }

    # Отправка запроса
    response = requests.post(url, params=params)
    # Обработка ответа
    data = response.json()
    if "response" in data:
        print(f"Пост опубликован! ID поста: {data['response']['post_id']}")
        return f"vk.ru/wall{pablik_id}_{data['response']['post_id']}"
    else:
        print(f"Ошибка: {data.get('error', 'Неизвестная ошибка')}")


def upload_photo(img_url):
    version = '5.199'
    album_id = 'nuh uh'
    access_token = 'nuh uh'
    pablik_id = 'nuh uh'
    upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        "access_token": access_token,
        "album_id": 'nuh uh',
        "v": version,
    }
    response = requests.get(upload_url, params=params)
    data = response.json()
    upload_url = data['response']['upload_url']
    # Шаг 2: Загружаем фотографию
    file_path = f'{img_url}'  # Путь к вашему изображению
    with open(file_path, 'rb') as f:
        files = {'file': f}
        upload_response = requests.post(upload_url, files=files)
        upload_data = upload_response.json()
    # Шаг 3: Сохраняем фотографию
    save_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'server': upload_data['server'],
        'photo': upload_data['photo'],
        'hash': upload_data['hash'],
        'v': '5.199'
    }
    save_response = requests.post(save_url, params=params)
    save_data = save_response.json()
    print(save_data)
    # Получаем id фотографии, которая будет прикреплена к посту
    photo = save_data['response'][0]
    owner_id = photo['owner_id']
    photo_id = photo['id']
    print(owner_id, photo_id)  # подвязывается на меня надо на паблик
    return owner_id, photo_id


def search_photo(ACCESS_KEY, search_tags):
    headers_post = {"Authorization": f"Client-ID {ACCESS_KEY}"}
    DOMAIN_UNSPLASH = 'https://api.unsplash.com'

    image_urls = []

    for search_tag in search_tags:
        if search_tag:
            params = {
                'page': 1,
                'query': search_tag,
                'orientation': 'landscape',
                'per_page': 10
            }
            url = f'{DOMAIN_UNSPLASH}/search/photos'

            print(f'Ищем фотографии по тегам...')
            response = requests.get(url, headers=headers_post, params=params)

            for i in range(0, 2):
                random_number = random.randint(0, 9)
                print(response.json())
                if response.json()['results']:
                    if random_number <= len(response.json()['results']):
                        if response.json()['results'][random_number]['urls'].get('full'):
                            image_urls.append(response.json()['results'][random_number]['urls']['full'])

    if len(image_urls) != 0:
        print(f'В выборку добавлено {len(image_urls)} изображений')
    else:
        print('Фотографии не найдены. Возвращаем заглушку')
        params = {
            'page': 1,
            'query': 'office',
            'orientation': 'landscape',
            'per_page': 10
        }
        response = requests.get(url, headers=headers_post, params=params)
        for i in range(0, 6):
            random_number = random.randint(0, 9)
            if response.json()['results'][random_number]['urls'].get('full'):
                image_urls.append(response.json()['results'][random_number]['urls']['full'])

        print('Заглушка найдена')
    if len(image_urls) != 0:
        return image_urls
    else:
        return None


# тестовый код отправки фото в вк (Фото кидается в альбом -> получается оттуда хэш и прочие данные для фото -> данные фото добавляются к посту)
options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.set_preference("general.useragent.override",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0")
driver = webdriver.Firefox(options=options)
driver.maximize_window()
screen_height = driver.execute_script("return window.screen.height;")
screen_width = driver.execute_script("return window.screen.width;")
print(screen_height, screen_width)

TOKEN = 'nuh uh'
CHANNEL_ID = '@test_true'
IMG_KEY = 'nuh uh'
bot = telebot.TeleBot(TOKEN)
choosen_news = []
users_await = {}


@bot.message_handler(commands=['start'])
def start(message):
    # https://stepik.org/lesson/870035/step/3 markdown для тг
    bot.send_message(message.chat.id, f'*Здравствуйте, {message.from_user.first_name}*', parse_mode='MarkdownV2')
    bot.send_message(message.chat.id,
                     '*Этот бот поможет вам отобрать новости 🗞 по вашим критериям с таких информационных источников как: *',
                     parse_mode='MarkdownV2')
    bot.send_message(message.chat.id,
                     '*\- Коммерсант\n\- РБК\n\- Госдума\n\- Право\.ру\n\- Следком\n\- Конституционный суд\n\- Федеральная палата адвокатов\n\- ФСБ*',
                     parse_mode='MarkdownV2')
    bot.send_message(message.chat.id,
                     '*Напишите на какую тему вы хотите выбрать новости 📰 из этих источников, и бот отправит вам подходящие варианты для публикации\. *☺️',
                     parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
def text(message):
    if str(message.chat.id) not in users_await:
        users_await[str(message.chat.id)] = False
        print(users_await, "if na false")
    print(users_await, "pered main")
    if users_await[str(message.chat.id)] != True:
        print(message.text)
        users_await[str(message.chat.id)] = True
        print(users_await, "generate")
        prompt = "Ты бот, твоя задача заключается в подборе необходимых новостей относительно выбора пользователя. "
        prompt += "Далее тебе будет отображён список новостей, из который ты должен брать всю информацию, ни откуда кроме этого списка новостей ты информацию брать НЕ МОЖЕШЬ, "
        prompt += "если ты не можешь найти подходящую новость то возвращаешь 'None', твой ответ должен представлять собой номер новостей, что ты считаешь подходящими для запроса пользователя, "
        prompt += "ничего кроме запятых и цифр в ответе не должно быть. Если тебя попросил отправить все новости, то ты должен выбрать не больше 20и новостей. Так же помни, что СВО (Или сво/Сво) - означает война. Вот список новостоей, из которых ты долежн предлагать пользователю новости: " + news_botu
        prompt += f"Тема которую выбрал пользователь: {message.text}"
        gen = bot.send_message(message.chat.id, "Генерируем новости...")
        gen_id = gen.message_id
        # Получаем ответ в формате [номер новости, номер новости2...., номер новстиN]
        cds_news = get_answer(prompt)
        if cds_news:
            choosen = []
            for id, i in enumerate(cds_news):
                i = int(i)
                # Формируем заголовок, если его нет, генерируем через GPT
                # title = news_all[i]['title'] or gpt('Придумай краткий и эффектный заголовок для этой новости: ', news_all[i]['desc'])

                bot.edit_message_text(chat_id=message.chat.id, message_id=gen_id,
                                      text=f'*Сгенерировано новостей: {id}*', parse_mode='MarkdownV2')
                # title = gpt('Не добавляй в текст ничего кроме того, что тебе сказали. Придумай краткий и эффектный заголовок НА РУССКОМ ЯЗЫКЕ для этой новости (Отправь ТОЛЬКО ТЕКСТ ЗАГОЛОВКА, не надо писать "Заголовок Заголовок новости", просто отправь заголовок который ты сгенерировал и всё): ', news_all[i]['desc'])
                choosen.append(f"{id + 1}. {news_all[i]['title']}")
                print("choosen")
                # news_all[i]["title"] = title
            bot.edit_message_text(chat_id=message.chat.id, message_id=gen_id,
                                  text="*Выбранные новости по вашему запросу: *", parse_mode='MarkdownV2')

            for count, news_text in enumerate(choosen):
                # Создаем разметку с одной кнопкой
                markup = InlineKeyboardMarkup()
                button = InlineKeyboardButton(f"Новость {count + 1}", callback_data=f'news_{cds_news[count]}')
                markup.add(button)
                bot.send_message(message.chat.id, news_text, reply_markup=markup)
                # Отправляем сообщение с текстом новости и кнопкой
            users_await[str(message.chat.id)] = False
        else:
            bot.delete_message(message.chat.id, gen_id)
            bot.send_message(message.chat.id,
                             "Не смогли получить список новостей ❌, повторите запрос переработав тему, которую вы запрашиваете")
            users_await[str(message.chat.id)] = False
    else:
        bot.send_message(message.chat.id, "Подождите немного! ❌ Ваш ответ ещё генерируется")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global resp, text_tg  # Делаем переменную глобальной для доступа из разных частей
    response = ""

    if call.data.startswith('news_') or call.data.startswith('btn'):
        if call.data.startswith('btn'):
            bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем сообщение о подтверждении
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        index = call.data.split('_')[1]
        index = int(index)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Да ✅", callback_data=f'confirm_{index}'))
        markup.add(InlineKeyboardButton("Нет ❌", callback_data=f'cancel_{index}'))
        markup.add(InlineKeyboardButton("Переработать всё 🔄", callback_data=f'btnrewrite_{index}'))
        markup.add(InlineKeyboardButton("Переработать текст 📃", callback_data=f'btntext_{index}'))
        markup.add(InlineKeyboardButton("Переработать фото 📸", callback_data=f'btnphoto_{index}'))
        if call.data.startswith("news"):
            gen = bot.send_message(call.message.chat.id, "*Генерируем текст и фото\.\.\.*", parse_mode='MarkdownV2')
            gen_id = gen.message_id
        elif call.data.startswith("btnphoto"):
            gen = bot.send_message(call.message.chat.id, "*Генерируем фото\.\.\.*", parse_mode='MarkdownV2')
            gen_id = gen.message_id
        elif call.data.startswith("btntext"):
            gen = bot.send_message(call.message.chat.id, "*Генерируем текст\.\.\.*", parse_mode='MarkdownV2')
            gen_id = gen.message_id
        elif call.data.startswith("btnrewrite"):
            gen = bot.send_message(call.message.chat.id, "*Генерируем текст и фото\.\.\.*", parse_mode='MarkdownV2')
            gen_id = gen.message_id
        if call.data.startswith('btnphoto') or call.data.startswith('news') or call.data.startswith('btnrewrite'):
            for i in range(5):
                try:
                    tags = make_tags(news_all[index]["desc"])
                    img_link = choose_best_image(search_photo(IMG_KEY, tags), news_all[index]["desc"])
                    news_all[index]["img_link"] = img_link
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=gen_id,
                                          text='*Фото сгенерировано\!* ✅', parse_mode='MarkdownV2')
                    print('img', img_link)
                    break
                except Exception as e:
                    print("error img:", e)

            try:
                file_name = r"/content/photo_usr.png"
                response = requests.get(img_link)
                if response.status_code == 200:
                    with open(file_name, "wb") as file:
                        file.write(response.content)
                        print(f"Фото успешно скачано и сохранён как {file_name}")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=gen_id,
                                              text='*Фото успешно сгенерировано и скачано\!* ✅',
                                              parse_mode='MarkdownV2')
                else:
                    print(f"Не удалось скачать фото. Ошибка: {response.status_code}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        if call.data.startswith('btntext') or call.data.startswith('news') or call.data.startswith('btnrewrite'):
            news_all[index]["desc"] = (describe(news_all[index]["desc"] if news_all[index]["desc"] else ""))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=gen_id,
                                  text='*Текст успешно сгенерирован\!* ✅', parse_mode='MarkdownV2')
            resp = response  # Сохраняем значение в глобальной переменной
            title_tg = rework_mark(news_all[index]["title"])
            desc_tg = rework_mark(news_all[index]["desc"])
            link_tg = rework_mark(news_all[index]["link"])
            date_tg = rework_mark(news_all[index]["date"])
            img_tg = rework_mark(news_all[index]["img_link"])
            text = f"*{title_tg}*\n\n{desc_tg}\n\n{date_tg}\n[Ссылка на новость]({link_tg})\n[Ссылка на изображение]({img_tg})"
            text_tg = text
        bot.delete_message(call.message.chat.id, gen_id)
        photoreal = open(r'/content/photo_usr.png', 'rb')
        bot.send_photo(call.message.chat.id, photo=photoreal, caption=text_tg, parse_mode='MarkdownV2')
        photoreal.close()
        bot.send_message(call.message.chat.id, "Вы уверены, что хотите отправить эту новость?", reply_markup=markup)
    elif call.data.startswith('confirm_'):
        index = call.data.split('_')[1]  # Получаем индекс новости
        index = int(index)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        published = ""
        title = news_all[index]["title"]
        desc = news_all[index]["desc"]
        date = news_all[index]["date"]
        link = news_all[index]["link"]
        link_img_v = news_all[index]["img_link"]
        text = f"{title}\n\n{desc}\n\n{date}\n{link_img_v}"
        # Отправляем начальное сообщение и сохраняем его ID
        sent_message = bot.send_message(call.message.chat.id, "Начинаем публикацию новостей...")
        message_id = sent_message.message_id  # ID сообщения
        chat_id = call.message.chat.id  # ID чата

        # Отправка в Telegram
        try:
            photoreal = open(r'/content/photo_usr.png', 'rb')
            tg_message = bot.send_photo(chat_id=CHANNEL_ID, photo=photoreal, caption=text_tg, parse_mode='MarkdownV2')
            photoreal.close()
            tg_message_id = tg_message.message_id
            link = f"https://t.me/{CHANNEL_ID.replace('@', '')}/{tg_message_id}"
            published += "*Новость успешно отправлена в Телеграм\!* ✅\n"
            published += f"Ссылка: [Нажмите]({rework_mark(link)})\n"
            print("НОВОСТЬ ДОБАВЛЕНА В ТГ")
        except Exception as e:
            print("Ошибка Telegram:", e)
            published += "*Не удалось отправить новость в Телеграм* ❌\n"

        # Обновляем сообщение
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=published, parse_mode='MarkdownV2')

        # Отправка в VK
        try:
            print("Постим в VK")
            owner_id, media_id = upload_photo(r"/content/photo_usr.png")
            vk_link = vk_posting(text, owner_id, media_id)
            published += "*Новость успешно отправлена в VK\!* ✅\n"
            published += f"Ссылка: [Нажмите]({rework_mark(vk_link)})\n"
            print("НОВОСТЬ ДОБАВЛЕНА НА ВК")
        except Exception as e:
            print("Ошибка VK:", e)
            published += "*Не удалось отправить новость в VK* ❌\n"

        # Обновляем сообщение
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=published, parse_mode='MarkdownV2')

        # Отправка в Twitter
        try:
            print("Постим в Twitter")
            text_x = text if len(
                text) < 240 else f"Заголовок: {news_all[index]['title']}\nДата: {news_all[index]['date']}\nСсылка: {news_all[index]['link']}"
            login_x("mail", "pass", "nick")
            twitter_link = post_x(text_x, "nick")
            published += "*Новость успешно отправлена в Твиттер\!* ✅\n"
            published += f"Ссылка: [Нажмите]({rework_mark(twitter_link)})\n"
            print("НОВОСТЬ ДОБАВЛЕНА НА ТВИТТЕР")
        except Exception as e:
            print("Ошибка Twitter:", e)
            published += "*Не удалось отправить новость в Твиттер* ❌\n"

        # Обновляем сообщение
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=published, parse_mode='MarkdownV2')

        # Отправка в Facebook
        try:
            login_fb("nick", "pass")
            link_fb = post_fb(text)
            published += "*Новость успешно отправлена в Facebook\!* ✅\n"
            published += f"Ссылка: [Нажмите]({rework_mark(link_fb)})\n"
            print("НОВОСТЬ ДОБАВЛЕНА НА ФЕЙСБУК")
        except Exception as e:
            print("Ошибка Facebook:", e)
            published += "*Не удалось отправить новость в Facebook* ❌\n"

        # Обновляем сообщение
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=published, parse_mode='MarkdownV2')

        # Отправка в Instagram
        try:
            login_inst("nick", "pass")
            link_inst = post_inst(text, "nick", r"/content/photo_usr.png")
            published += "*Новость успешно отправлена в Instagram\!* ✅\n"
            published += f"Ссылка: [Нажмите]({rework_mark(link_inst)})\n"
            print("НОВОСТЬ ДОБАВЛЕНА В ИНСТУ")
        except Exception as e:
            print("Ошибка Instagram:", e)
            published += "*Не удалось отправить новость в Instagram* ❌\n"

        # Финальное обновление сообщения
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=published, parse_mode='MarkdownV2')

    elif call.data.startswith('cancel_'):
        bot.send_message(call.message.chat.id,
                         "Действие отменено. Задайте новую тему если хотите снова выбрать новость")
        bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем сообщение о подтверждении
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)


# while True:
#   try:
#     bot.polling()
#   except:
# for i in range(10):
#   try:
bot.polling()

# except:
#   print("ueeee")
# users_await = {}
