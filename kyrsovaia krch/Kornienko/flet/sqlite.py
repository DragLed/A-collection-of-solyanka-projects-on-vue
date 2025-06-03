import telebot
import sqlite3

bot = telebot.TeleBot('7069232805:AAHu5aEEBMmkwoyoazg-6nBDUUiwQrQpXF4')


@bot.message_handler(commands=["start"])
def start(message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Выполнить запрос для получения всех данных из таблицы USERTG
    c.execute("SELECT * FROM USERTG")
    results = c.fetchall()

    if results:
        response = "\n".join([str(result) for result in results])
        bot.send_message(message.chat.id, f"All data:\n{response}\t\t\t\n\n\n")
    else:
        bot.send_message(message.chat.id, "No data found in the table.")

    conn.close()

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
    print(f"Новое сообщение!!!!!  >>>  {message.text} от {message.from_user.username}")
    bot.send_message(message.chat.id, "Ваше сообщение было отправлено на главную консоль нашему разработчику")

bot.infinity_polling()
