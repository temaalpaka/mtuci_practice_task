import telebot
from telebot import types
import requests

TOKEN = '*****'  #Токен телеграмм бота (Скрыт)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])  #Приветствие по команде /start - Запустить/Перезапустить бота
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, 'Здравствуй, {0.first_name}!'.format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, 'Это бот для поиска вакансий, резюме и их анализа с помощью DB, на основе API hh.ru.'.format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, 'Что бы продолжить, выбери необходимую тебе команду, в предложенном меню ниже'.format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['resume']) #По команде /resume
def welcome(message):
    mesg = bot.send_message(message.chat.id,'Пожалуйста, введите необходимое резюме.')
    bot.register_next_step_handler(mesg,test)
def test(message):
    bot.send_message(message.chat.id,'Спасибо, запрос принят.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('↩️Назад↩️')
    markup.add(back)
    stick = open('ПОИСК.png', 'rb')
    bot.send_sticker(message.chat.id, stick, reply_markup=markup)

    def get_resumes(keyword):
        url = "https://api.hh.ru/resumes"
        params = {
            "text": keyword,
            "area": 1,  #id Города (1 - Москва и так далее по списку (2 - Питер и тд))
            "per_page": 5,  #Количество найденных резюме в ответе
        }
        headers = {
            "User-Agent": "Your User Agent",  # Replace with your User-Agent header
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            resumes = data.get("items", [])
            for resume in resumes:
                #Необходимая информация из резюме
                resume_id = resume.get("id")
                resume_url = resume.get("alternate_url")
                resume_block_title_position = resume.get("position")
                bloko_header_2 = resume.get("experience", {}).get("name")
                resume_personal_gender = resume.get("name")
                resume_personal_age = resume.get("age")
                bot.send_message(message.chat.id,
                                 f"ID: {resume_id}\nURL: {resume_url}\nДолжность: {resume_block_title_position}\nОпыт: {bloko_header_2}\nПол: {resume_personal_gender}\nВозраст: {resume_personal_age}\n",
                                 reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"Request failed with status code: {response.status_code}",
                             reply_markup=markup)

    #bot.send_message(message.chat.id, 'Введите необходимое вам резюме', reply_markup=markup)
    get_resumes(message.text)  #Ввод резюме

@bot.message_handler(commands=['vacancy']) #По команде /vacancy
def welcome(message):
    mesg = bot.send_message(message.chat.id,'Пожалуйста, введите необходимую вакансию.')
    bot.register_next_step_handler(mesg,test)

def test(message):
    bot.send_message(message.chat.id,'Спасибо, запрос принят.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('↩️Назад↩️')
    markup.add(back)
    stick = open('ПОИСК.png', 'rb')
    bot.send_sticker(message.chat.id, stick, reply_markup=markup)
    def get_vacancies(keyword):
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,
            "area": 1,  #id Города (1 - Москва и так далее по списку (2 - Питер и тд))
            "per_page": 5,  #Количество найденных вакансий в ответе
        }
        headers = {
            "User-Agent": "Your User Agent",  #Replace with your User-Agent header
        }

        # args = []
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            for vacancy in vacancies:
                #Необходимая информация из вакансии
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")
                #vacancy_salary_compensation_type_net = vacancy.get("salary", {}).get("from") Pay: {vacancy_salary_compensation_type_net}\n Не во всех вакансиях указана зарплата
                #vacancy_viewers_count = vacancy.get("") Viewers: {vacancy_viewers_count}\n Не смог найти правильное обозначение этой функции
                vacancy_description_list_item = vacancy.get("employment", {}).get("name")
                vacancy_experience = vacancy.get("experience", {}).get("name")
                bot.send_message(message.chat.id, f"ID: {vacancy_id}\nURL: {vacancy_url}\nДолжность: {vacancy_title}\nКомпания: {company_name}\nОпыт работы: {vacancy_experience}\nФормат: {vacancy_description_list_item}\n", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"Request failed with status code: {response.status_code}", reply_markup=markup)

    #bot.send_message(message.chat.id, 'Введите необходимую вам вакансию', reply_markup=markup)
    get_vacancies(message.text)  #Ввод вакансии

@bot.message_handler(commands=['menu'])  #Меню с кнопками по команде /menu - Основное меню
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('ℹ️Инфоℹ️')
    item2 = types.KeyboardButton('🛠️Работа🛠️')
    item3 = types.KeyboardButton('⚙️Другое⚙️')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Основное меню:'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])  #Меню с кнопками по команде /menu - Основное меню
def messy(message):
    if message.chat.type == 'private':
        if message.text == 'ℹ️Инфоℹ️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🤖О боте🤖')
            item2 = types.KeyboardButton('📍Команды📍')
            back = types.KeyboardButton('↩️Назад↩️')
            markup.add(item1, item2, back)
            stick = open('ИНФОРМАЦИЯ.png', 'rb')
            bot.send_sticker(message.chat.id, stick, reply_markup=markup)

        elif message.text == '🛠️Работа🛠️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🔎Вакансии🔎')
            item2 = types.KeyboardButton('📊Аналитика вакансии📊')
            item3 = types.KeyboardButton('🔎Резюме🔎')
            back = types.KeyboardButton('↩️Назад↩️')
            markup.add(item1, item2, item3, back)
            stick = open('РАБОТА.png', 'rb')
            bot.send_sticker(message.chat.id, stick, reply_markup=markup)

        elif message.text == '↩️Назад↩️':  #Кнопка возвращающая в первое меню
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('ℹ️Инфоℹ️')
            item2 = types.KeyboardButton('🛠️Работа🛠️')
            item3 = types.KeyboardButton('⚙️Другое⚙️')
            markup.add(item1, item2, item3)
            stick = open('НАЗАД.png', 'rb')
            bot.send_sticker(message.chat.id, stick, reply_markup=markup)

        elif message.text == '⚙️Другое⚙️':  #Кнопка для теста и наработок
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('↩️Назад↩️')
            markup.add(back)
            bot.send_message(message.chat.id, 'Пока не работает', reply_markup=markup)
            # bot.send_message(message.chat.id, '*' + str(random.randint(0, 10))) #Тестировал функции
            # stick = open('scale.png','rb')
            # bot.send_sticker(message.chat.id, stick)

        elif message.text == '📍Команды📍':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('↩️Назад↩️')
            markup.add(back)
            stick = open('КОМАНДЫ.png', 'rb')
            bot.send_sticker(message.chat.id, stick, reply_markup=markup)
            bot.send_message(message.chat.id, 'Доступные команды: /start - Запустить/Перезапустить бота; /vacancy - Поиск Вакансий по запросу; /resume - Поиск Резюме по запросу; /menu - Основное меню', reply_markup=markup)

        elif message.text == '🤖О боте🤖':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('↩️Назад↩️')
            markup.add(back)
            stick = open('О БОТЕ.png', 'rb')  #Доп. оформление которое бот отправляет в ответ на запрос кнопки, в виде стикеров телеграмм
            bot.send_sticker(message.chat.id, stick, reply_markup=markup)
            bot.send_message(message.chat.id, 'Бот был создан для Практического задания от МТУСИ', reply_markup=markup)

        elif message.text == '🔎Вакансии🔎':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('↩️Назад↩️')
            markup.add(back)
            stick = open('ПОИСК.png', 'rb')
            bot.send_sticker(message.chat.id, stick, reply_markup=markup)

bot.polling(none_stop=True)  #Что бы телеграмм бот работал постоянно (Не выключался после первой команды)