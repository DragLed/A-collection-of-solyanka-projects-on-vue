import telebot 
import time

bot = telebot.TeleBot('7554567043:AAFMvv6HXYXGfhub8gD5qc3fIGjnApJinFI')

def send_message_love(chat_id):
    bot.send_message(chat_id, "Люблю тебя 💖💖💖")

@bot.message_handler(commands=['start'])
def send_startmessage(message):
    bot.send_message(message.chat.id, "lol")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "spam":
        i = 0
        while True:
            if i != 100:
                time.sleep(0.2)
                bot.send_message(6629738276, f"Люблю тебя)) 💖💝💗")
                i = i + 1
    


bot.polling(none_stop=True)