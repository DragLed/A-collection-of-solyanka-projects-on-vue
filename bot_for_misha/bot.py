import telebot
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = telebot.TeleBot('6454664810:AAEv7EBHyP9gdLPJ1xyTRgnOBhoCyUSeXrI')
db = sqlite3.connect('bd.db')
c = db.cursor()


# c.execute("""CREATE TABLE product2 (
#     name text,
#     price integer
#
#
# )""")
# c.execute('INSERT INTO product VALUES ("Kapot TRX",21075)')
# c.execute('INSERT INTO product VALUES ("Reshetka na steklo + polka/stolik. Haval",15780)')
# c.execute('INSERT INTO product VALUES ("Zachita bampera H5",19715)')
# c.execute('INSERT INTO product VALUES ("Videoregistr H5",6120)')
# c.execute('INSERT INTO product VALUES ("Porogi allumin + plastik H5",22000)')
# c.execute('INSERT INTO product VALUES ("Electrobagajhik H5",29500)')
# c.execute('INSERT INTO product VALUES ("Nakladki na bamper H9",8500)')
# c.execute('INSERT INTO product VALUES ("Nakladka na reshetky+fari+podsvetka mat chern. H9",21000)')
# c.execute('INSERT INTO product VALUES ("Dovodchik zadnei dveri H9",12500)')
# c.execute('INSERT INTO product VALUES ("lebedka H9",35350)')

db.commit()

user_positions = {}



@bot.message_handler(commands=['start'])
def start(message):
    user_positions[message.chat.id] = 1
    bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + ", я бот который поможет легко и быстро сделать заказ в магазине.")

@bot.message_handler(commands=['search'])
def search(message):
    db = sqlite3.connect('bd.db')
    c = db.cursor()
    print(f"Пользователь @{message.from_user.username} импользывал команду /search")
    i = user_positions[message.chat.id]
    c.execute(f"SELECT rowid, * FROM product")
    items = c.fetchall()
    c.execute(f"SELECT rowid, * FROM product WHERE rowid == {i}")
    item = c.fetchone()
    markup = InlineKeyboardMarkup(row_width=2)
    buttonnext = InlineKeyboardButton("Вперёд ➡️", callback_data="next")
    butN = InlineKeyboardButton("Подробнее", callback_data="toItem")
    markup.add(butN, buttonnext)
    bot.send_photo(message.chat.id, photo=open("photo_2024-12-16_00-38-07.jpg", "rb"),
                        caption=f"🛠 Товар: {item[1]}\n💰 Цена: {item[2]} руб.", reply_markup=markup)

    db.close()


db.commit()

@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next", "toItem"])
def handle_callback(call):
    i = user_positions[call.message.chat.id]
    if call.data == "next":
        i += 1
        user_positions[call.message.chat.id] = i
    elif call.data == "prev":
        i -= 1
        user_positions[call.message.chat.id] = i
    elif call.data == "toItem":
        rulet = False
        bot.send_message(call.message.chat.id, "Бездарь")
    db = sqlite3.connect('bd.db')
    c = db.cursor()
    c.execute(f"SELECT rowid, * FROM product")
    items = c.fetchall()
    if i < len(items) and i > 1:
        c.execute(f"SELECT rowid, * FROM product WHERE rowid == {i}")
        item = c.fetchone()
        markup = InlineKeyboardMarkup(row_width=2)
        buttonprev = InlineKeyboardButton("⬅️ Назад", callback_data="prev")
        buttonnext = InlineKeyboardButton("Вперёд ➡️", callback_data=f"next")
        butN = InlineKeyboardButton("Подробнее", callback_data="toItem")
        markup.add(buttonprev, buttonnext, butN)
        bot.send_photo(call.message.chat.id, photo=open("photo_2024-12-16_00-38-07.jpg", "rb"),
                       caption=f"🛠 Товар: {item[1]}\n💰 Цена: {item[2]} руб.", reply_markup=markup)
    elif i == 1:
        c.execute(f"SELECT rowid, * FROM product WHERE rowid == {i}")
        item = c.fetchone()
        markup = InlineKeyboardMarkup(row_width=2)
        buttonnext = InlineKeyboardButton("Вперёд ➡️", callback_data=f"next")
        butN = InlineKeyboardButton("Подробнее", callback_data="toItem")
        markup.add(butN, buttonnext)
        bot.send_photo(call.message.chat.id, photo=open("photo_2024-12-16_00-38-07.jpg", "rb"),
                       caption=f"🛠 Товар: {item[1]}\n💰 Цена: {item[2]} руб.", reply_markup=markup)
        rulet = False
    elif i == len(items):
        c.execute(f"SELECT rowid, * FROM product WHERE rowid == {i}")
        item = c.fetchone()
        markup = InlineKeyboardMarkup(row_width=2)
        buttonprev = InlineKeyboardButton("⬅️ Назад", callback_data="prev"),
        butN = InlineKeyboardButton("Подробнее", callback_data="toItem")
        markup.add(buttonprev, butN)
        bot.send_photo(call.message.chat.id, photo=open("photo_2024-12-16_00-38-07.jpg", "rb"),
                       caption=f"🛠 Товар: {item[1]}\n💰 Цена: {item[2]} руб.", reply_markup=markup)
        rulet = False
    else:
        print(f"У пользователя {call.message.from_user.username}ошибка с товаром")

    db.close()


db.close()
bot.polling()