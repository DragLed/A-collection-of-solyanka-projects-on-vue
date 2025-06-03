import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import sqlite3

bot = telebot.TeleBot('6454664810:AAEv7EBHyP9gdLPJ1xyTRgnOBhoCyUSeXrI')
db = sqlite3.connect('bd.db', check_same_thread=False)
c = db.cursor()

user_positions = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_positions[message.chat.id] = 1
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я помогу легко и быстро сделать заказ.\n\nНажми на →/search←")


@bot.message_handler(commands=['search'])
def search(message):
    user_positions[message.chat.id] = 1
    show_product(message.chat.id, 1)


@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next", "toItem"])
def handle_callback(call):
    user_id = call.message.chat.id
    current_pos = user_positions.get(user_id, 1)

    if call.data == "next":
        current_pos += 1
    elif call.data == "prev":
        current_pos -= 1
    elif call.data == "toItem":
        bot.send_message(user_id, "Подробнее о товаре скоро будет доступно.")
        return

    user_positions[user_id] = max(1, current_pos)
    show_product(user_id, user_positions[user_id], call)


def show_product(chat_id, position, call=None):
    c.execute("SELECT COUNT(*) FROM product")
    total_items = c.fetchone()[0]

    if position > total_items:
        position = total_items
    elif position < 1:
        position = 1

    c.execute(f"SELECT rowid, * FROM product WHERE rowid = ?", (position,))
    item = c.fetchone()

    if not item:
        bot.send_message(chat_id, "Товар не найден.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    if position > 1:
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="prev"))
    if position < total_items:
        markup.add(InlineKeyboardButton("Вперёд ➡️", callback_data="next"))
    markup.add(InlineKeyboardButton("Подробнее", callback_data="toItem"))

    photo_path = "photo_2024-12-16_00-38-07.jpg"

    try:
        if call:
            # Редактируем сообщение
            bot.edit_message_media(
                media=InputMediaPhoto(open(photo_path, "rb"),
                                      caption=f"🛠 Товар: {item[1]}\n💰 Цена: {item[2]} руб."),
                chat_id=chat_id,
                message_id=call.message.message_id,
                reply_markup=markup
            )
        else:
            # Отправляем новое сообщение
            bot.send_photo(
                chat_id=chat_id,
                photo=open(photo_path, "rb"),
                caption=f"🛠 Товар: {item[1]}\n💰 Цена: {item[2]} руб.",
                reply_markup=markup
            )
    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка при загрузке товара.")
        print(f"Ошибка: {e}")


bot.polling()