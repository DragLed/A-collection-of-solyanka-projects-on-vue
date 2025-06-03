import telebot
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import time
import threading
import time
import pprint
import json
import os
import threading

bot = telebot.TeleBot('7785904059:AAG-OTrvGZEmePPKiOHUwZpmTs3THcnL2qY')  # Замените на свой токен
ref_link = 'https://t.me/{}?start={}'
DATA_FILE = 'user_data.json'
user_data = {}
data_lock = threading.Lock()

def load_user_data():
    global user_data
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                user_data = json.load(file)
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")

def save_user_data():
    try:
        with data_lock:
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def generate_day_keyboard():
    markup = InlineKeyboardMarkup(row_width=7)
    buttons = [InlineKeyboardButton(str(i), callback_data=f"day:{i}") for i in range(1, 32)]
    markup.add(*buttons)
    return markup

def generate_month_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    buttons = [InlineKeyboardButton(month, callback_data=f"month:{i + 1}") for i, month in enumerate(months)]
    markup.add(*buttons)
    return markup

def generate_year_keyboard():
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = [InlineKeyboardButton(str(year), callback_data=f"year:{year}") for year in range(2020, 2030)]
    markup.add(*buttons)
    return markup

def print_user_data():
    print("Текущие данные пользователей:")
    pprint.pprint(user_data)

def send_date_difference():
    try:
        today = datetime.now()
        for user_id, data in user_data.items():
            if 'day' in data and 'month' in data and 'year' in data:
                selected_date = datetime(year=int(data['year']), month=int(data['month']), day=int(data['day']))
                difference = (today - selected_date).days
                bot.send_message(user_id, f"Вашей паре: {difference} дней.")
    except Exception as e:
        print(f"Ошибка при отправке данных пользователю: {e}")

def delete_user_data(user_id):
    global user_data
    if user_id in user_data:
        bot.send_message(user_id, "Вы уверены, что хотите удалить ваши данные? Напишите 'да' для подтверждения.")
        bot.register_next_step_handler_by_chat_id(user_id, confirm_deletion)
    else:
        print(f"Пользователь с ID {user_id} не найден в данных.")

def confirm_deletion(message):
    user_id = message.chat.id
    if message.text.lower() == 'да':
        del user_data[user_id]  # Удаляем данные пользователя из словаря
        save_user_data()  # Сохраняем обновленные данные в файл
        bot.send_message(user_id, "Ваши данные успешно удалены.")
        print(f"Данные пользователя {user_id} успешно удалены.")
    else:
        bot.send_message(user_id, "Удаление данных отменено.")


def send_daily_message():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=14, minute=0, second=0, microsecond=0)

        # Если сейчас уже позже 14:00, смещаем время на следующий день
        if now > target_time:
            target_time += timedelta(days=1)

        # Рассчитываем время до следующего уведомления
        time_to_wait = (target_time - now).total_seconds()
        print(f"Ждём до 14:00. Осталось {time_to_wait} секунд.")

        # Ждём до 14:00
        time.sleep(time_to_wait)

        # Отправляем сообщение всем пользователям
        try:
            today = datetime.now()
            for user_id, data in user_data.items():
                if 'day' in data and 'month' in data and 'year' in data:
                    selected_date = datetime(year=int(data['year']), month=int(data['month']), day=int(data['day']))
                    difference = (today - selected_date).days
                    bot.send_message(user_id, f"Вы встречаетесь уже {difference} дней.")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

def start_scheduled_messages():
    message_thread = threading.Thread(target=send_daily_message)
    message_thread.daemon = True  # Сделаем поток демоном, чтобы он завершался с основным процессом
    message_thread.start()


@bot.message_handler(commands=['start'])
def send_startmessage(message):
    print(f"Пользователь {message.from_user.username} ввёл команду /start")
    load_user_data()  # Загружаем данные

    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "неизвестный пользователь"
    args = message.text.split()

    # Клавиатура (оставляем как было)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton("Сколько мы встречаемся?")
    button2 = types.KeyboardButton("Установить новую дату")
    button3 = types.KeyboardButton("Пригласить партнёра")
    keyboard.add(button1, button2, button3)

    # Если пользователь перешёл по реферальной ссылке
    if len(args) > 1:
        partner_id = args[1]  # ID пригласившего

        if partner_id in user_data:  # Если пригласивший существует
            if user_id not in user_data:  # Если текущий пользователь новый
                # Копируем данные партнёра (если есть)
                partner_data = user_data.get(partner_id, {})
                user_data[user_id] = {
                    'username': username,
                    'partner_id': partner_id,
                    'day': partner_data.get('day'),
                    'month': partner_data.get('month'),
                    'year': partner_data.get('year'),
                }
                bot.send_message(user_id, f"Вы присоединились по приглашению пользователя {user_data[partner_id]['username']}.")
                save_user_data()
            else:
                bot.send_message(user_id, "Вы уже зарегистрированы.")
        else:
            bot.send_message(user_id, "Пользователь, который вас пригласил, не найден.")

    # Если пользователь не перешёл по ссылке и его ещё нет в базе
    if user_id not in user_data:
        user_data[user_id] = {'username': username}
        bot.send_message(user_id, "Привет! Этот бот поможет вам не забыть важные даты.", reply_markup=keyboard)
        save_user_data()
    else:
        bot.send_message(user_id, "С возвращением!", reply_markup=keyboard)



@bot.message_handler(commands=['date'])
def send_welcome(message):
    try:
        print(f"Пользователь {message.from_user.username} ввёл команду /date")
        user_id = message.chat.id
        username = message.from_user.username if message.from_user.username else "неизвестный пользователь"

        if user_id not in user_data:
            user_data[user_id] = {'username': username}
        else:
            bot.send_message(user_id, "Вы уже ввели данные ранее. Хотите изменить дату? Выберите день.")

        bot.send_message(user_id, "Выберите день, когда вы начали встречаться:", reply_markup=generate_day_keyboard())

        save_user_data()
    except Exception as e:
        print(f"Ошибка при обработке команды /date: {e}")

@bot.message_handler(commands=['check'])
def check_relationship_duration(message):
    print(f"Пользователь {message.from_user.username} ввёл команду /check")

    user_id = message.chat.id
    print(f"Пользователь {message.from_user.username} и с ID {user_id} ввёл команду /check")
    if user_id in user_data and 'day' in user_data[user_id] and 'month' in user_data[user_id] and 'year' in user_data[user_id]:
        selected_date = datetime(year=int(user_data[user_id]['year']),
                                 month=int(user_data[user_id]['month']),
                                 day=int(user_data[user_id]['day']))
        difference = (datetime.now() - selected_date).days
        bot.send_message(user_id, f"Вы встречаетесь уже {difference} дней.")
    else:
        bot.send_message(user_id, "Сначала введите дату вашей встречи с помощью команды /date.")


@bot.message_handler(commands=['invite'])
def invite_user(message):
    print(f"Пользователь {message.from_user.username} ввёл команду /invite")
    user_id = message.chat.id
    invite_link = ref_link.format(bot.get_me().username, user_id)
    bot.send_message(user_id, f"Пригласите вашего партнёра с помощью этой ссылки: {invite_link}")
    

@bot.message_handler(func=lambda message: True)
def ReplyKeyboardMarkup(message):
    if message.text == "Сколько мы встречаемся?":
        check_relationship_duration(message)

    elif message.text == "Установить новую дату":
        send_welcome(message)

    elif message.text == "Пригласить партнёра":
        invite_user(message)
        
        
@bot.callback_query_handler(func=lambda call: call.data.startswith("day"))
def handle_day_selection(call):
    user_id = call.message.chat.id
    day = call.data.split(":")[1]
    user_data[user_id]['day'] = day
    bot.send_message(user_id, f"Вы выбрали {day} число. Теперь выберите месяц.", reply_markup=generate_month_keyboard())
    save_user_data()

@bot.callback_query_handler(func=lambda call: call.data.startswith("month"))
def handle_month_selection(call):
    user_id = call.message.chat.id
    month = call.data.split(":")[1]
    user_data[user_id]['month'] = month
    bot.send_message(user_id, f"Вы выбрали {month} месяц. Теперь выберите год.", reply_markup=generate_year_keyboard())
    save_user_data()

@bot.callback_query_handler(func=lambda call: call.data.startswith("year"))
def handle_year_selection(call):
    user_id = call.message.chat.id
    year = call.data.split(":")[1]
    user_data[user_id]['year'] = year
    bot.send_message(user_id, f"Вы выбрали {year} год. Дата установлена.")
    save_user_data()


load_user_data()
start_scheduled_messages()
bot.polling(none_stop=True)
