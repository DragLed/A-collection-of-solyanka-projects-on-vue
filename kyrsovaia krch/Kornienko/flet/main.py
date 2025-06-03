import telebot
from telebot import types
from random import randint
import sqlite3

# Создаем таблицы, если они не существуют
conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS USERTG
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS GADALKA__ONLINE
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, namef TEXT, compatibility INTEGER)''')
conn.commit()
conn.close()

bot = telebot.TeleBot('6511341769:AAERXWzplolCm6-EmpVNMkOsqlytOlPWyNo')


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    user_telegramm = message.chat.id

    # Проверяем, существует ли пользователь
    c.execute("SELECT * FROM USERTG WHERE user = ?", (user_telegramm,))
    result = c.fetchone()

    if not result:
        # Если пользователя нет, добавляем его в базу данных
        c.execute("INSERT INTO USERTG (user) VALUES (?)", (user_telegramm,))
        conn.commit()

    conn.close()
    bot.send_message(message.chat.id, 'Введите своё имя и имя партнёра через пробел.')


@bot.message_handler(commands=["adv"])
def adv(message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Выполнить запрос для получения всех данных из столбца user таблицы USERTG
    c.execute("SELECT user FROM USERTG")
    results = c.fetchall()

    for result in results:
        try:
            # Отправить сообщение каждому id
            print("Сообщение отпралено")
            bot.send_message(result[0], "Подпишись на этот тг канал   https://t.me/PandaMishkaChina")
        except telebot.apihelper.ApiTelegramException as e:
            if e.result_json['error_code'] == 400:
                print("Пользователь заблокировал вас нахуй")

    conn.close()


@bot.message_handler(func=lambda message: True)

def handle_message(message):
    user_message = message.text.split(' ')
    if len(user_message) == 2:
        name1, name2 = user_message[0].lower(), user_message[1].lower()

        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Проверяем существующую совместимость
        c.execute("SELECT * FROM GADALKA__ONLINE WHERE name = ? AND namef = ?", (name1, name2))
        result = c.fetchone()

        if result:
            compatibility = result[3]  # Получаем совместимость из существующей записи
            print(f'Совместимость имён {name1} и {name2}: {compatibility}% ')
            bot.send_message(message.chat.id,
                             f'Совместимость имён {name1} и {name2}: {compatibility}% \n\n\n\nчтобы снова проверить совместимость, введите имена снова')
        else:
            compatibility = randint(50, 100)
            c.execute("INSERT INTO GADALKA__ONLINE (name, namef, compatibility) VALUES (?, ?, ?)",
                      (name1, name2, compatibility))
            c.execute("INSERT INTO GADALKA__ONLINE (name, namef, compatibility) VALUES (?, ?, ?)",
                      (name2, name1, compatibility))
            conn.commit()
            print(
                f'Совместимость имён {name1} и {name2}: {compatibility}%')
            bot.send_message(message.chat.id,
                             f'Совместимость имён {name1} и {name2}: {compatibility}%\n\n\n\nчтобы снова проверить совместимость, введите имена снова')

        conn.close()
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите два имени через пробел.')


bot.infinity_polling()
