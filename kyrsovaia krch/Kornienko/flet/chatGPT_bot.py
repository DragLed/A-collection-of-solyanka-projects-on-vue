import sqlite3
import telebot
from telebot import types

API_TOKEN = '6454664810:AAEv7EBHyP9gdLPJ1xyTRgnOBhoCyUSeXrI'
ADMIN_ID = 1698145451

bot = telebot.TeleBot(API_TOKEN)

# Database setup
conn = sqlite3.connect('shop.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS products
                  (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, photo TEXT, description TEXT)''')
conn.commit()

# States for product addition
class Product:
    def __init__(self):
        self.name = None
        self.category = None
        self.price = None
        self.photo = None
        self.description = None

product_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the shop bot! Use /add to add a new product, /edit to edit a product, /delete to delete a product, /list to list all products.")

@bot.message_handler(commands=['add'])
def add_product(message):
    product_data[message.chat.id] = Product()
    msg = bot.reply_to(message, "Enter the product name:")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    product_data[message.chat.id].name = message.text
    msg = bot.reply_to(message, "Enter the product category:")
    bot.register_next_step_handler(msg, process_category_step)

def process_category_step(message):
    product_data[message.chat.id].category = message.text
    msg = bot.reply_to(message, "Enter the product price:")
    bot.register_next_step_handler(msg, process_price_step)

def process_price_step(message):
    try:
        product_data[message.chat.id].price = float(message.text)
        msg = bot.reply_to(message, "Send the product photo:")
        bot.register_next_step_handler(msg, process_photo_step)
    except ValueError:
        msg = bot.reply_to(message, "Price must be a number. Enter the product price:")
        bot.register_next_step_handler(msg, process_price_step)

def process_photo_step(message):
    if message.content_type == 'photo':
        product_data[message.chat.id].photo = message.photo[-1].file_id
        msg = bot.reply_to(message, "Enter the product description:")
        bot.register_next_step_handler(msg, process_description_step)
    else:
        msg = bot.reply_to(message, "Please send a photo of the product.")
        bot.register_next_step_handler(msg, process_photo_step)

def process_description_step(message):
    product_data[message.chat.id].description = message.text

    cursor.execute("INSERT INTO products (name, category, price, photo, description) VALUES (?, ?, ?, ?, ?)",
                   (product_data[message.chat.id].name, product_data[message.chat.id].category,
                    product_data[message.chat.id].price, product_data[message.chat.id].photo,
                    product_data[message.chat.id].description))
    conn.commit()

    bot.reply_to(message, "Product added successfully!")
    bot.send_message(ADMIN_ID, f"New product added: {product_data[message.chat.id].name}")
    del product_data[message.chat.id]

@bot.message_handler(commands=['list'])
def list_products(message):
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    if products:
        for product in products:
            bot.send_photo(message.chat.id, product[4],
                           caption=f"ID: {product[0]}\nName: {product[1]}\nCategory: {product[2]}\nPrice: {product[3]}\nDescription: {product[5]}")
    else:
        bot.reply_to(message, "No products available.")

@bot.message_handler(commands=['edit'])
def edit_product(message):
    msg = bot.reply_to(message, "Enter the product ID to edit:")
    bot.register_next_step_handler(msg, process_edit_id_step)

def process_edit_id_step(message):
    try:
        product_id = int(message.text)
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if product:
            product_data[message.chat.id] = Product()
            product_data[message.chat.id].id = product_id

            msg = bot.reply_to(message, "Enter the new product name (or type 'skip' to keep current):")
            bot.register_next_step_handler(msg, process_edit_name_step)
        else:
            bot.reply_to(message, "Product not found. Please try again.")
    except ValueError:
        bot.reply_to(message, "Invalid ID. Please enter a valid product ID.")

def process_edit_name_step(message):
    if message.text.lower() != 'skip':
        product_data[message.chat.id].name = message.text

    msg = bot.reply_to(message, "Enter the new product category (or type 'skip' to keep current):")
    bot.register_next_step_handler(msg, process_edit_category_step)

def process_edit_category_step(message):
    if message.text.lower() != 'skip':
        product_data[message.chat.id].category = message.text

    msg = bot.reply_to(message, "Enter the new product price (or type 'skip' to keep current):")
    bot.register_next_step_handler(msg, process_edit_price_step)

def process_edit_price_step(message):
    if message.text.lower() != 'skip':
        try:
            product_data[message.chat.id].price = float(message.text)
        except ValueError:
            msg = bot.reply_to(message, "Price must be a number. Enter the new product price (or type 'skip' to keep current):")
            bot.register_next_step_handler(msg, process_edit_price_step)
            return

    msg = bot.reply_to(message, "Send the new product photo (or type 'skip' to keep current):")
    bot.register_next_step_handler(msg, process_edit_photo_step)

def process_edit_photo_step(message):
    if message.content_type == 'photo':
        product_data[message.chat.id].photo = message.photo[-1].file_id
    elif message.text.lower() == 'skip':
        pass
    else:
        msg = bot.reply_to(message, "Please send a photo of the product (or type 'skip' to keep current):")
        bot.register_next_step_handler(msg, process_edit_photo_step)
        return

    msg = bot.reply_to(message, "Enter the new product description (or type 'skip' to keep current):")
    bot.register_next_step_handler(msg, process_edit_description_step)

def process_edit_description_step(message):
    if message.text.lower() != 'skip':
        product_data[message.chat.id].description = message.text

    update_fields = []
    update_values = []

    if product_data[message.chat.id].name:
        update_fields.append("name = ?")
        update_values.append(product_data[message.chat.id].name)
    if product_data[message.chat.id].category:
        update_fields.append("category = ?")
        update_values.append(product_data[message.chat.id].category)
    if product_data[message.chat.id].price:
        update_fields.append("price = ?")
        update_values.append(product_data[message.chat.id].price)
    if product_data[message.chat.id].photo:
        update_fields.append("photo = ?")
        update_values.append(product_data[message.chat.id].photo)
    if product_data[message.chat.id].description:
        update_fields.append("description = ?")
        update_values.append(product_data[message.chat.id].description)

    if update_fields:
        update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(product_data[message.chat.id].id)
        cursor.execute(update_query, update_values)
        conn.commit()

    bot.reply_to(message, "Product updated successfully!")
    del product_data[message.chat.id]

@bot.message_handler(commands=['delete'])
def delete_product(message):
    msg = bot.reply_to(message, "Enter the product ID to delete:")
    bot.register_next_step_handler(msg, process_delete_id_step)

def process_delete_id_step(message):
    try:
        product_id = int(message.text)
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        bot.reply_to(message, "Product deleted successfully!")
    except ValueError:
        bot.reply_to(message, "Invalid ID. Please enter a valid product ID.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
