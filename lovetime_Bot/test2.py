from telethon import TelegramClient
import asyncio

# Ваши данные
api_id = 25979744
api_hash = '9a3ba25f624c0d71e1579044df9c81a6'
phone = '+79045085459'
password = '111281Nik'
chat_id = 6629738276  # ID целевого чата
session_name = 'userbot_session'

client = TelegramClient(session_name, api_id, api_hash)

async def send_message(text):
    try:
        await client.send_message(chat_id, text)
        print(f"✅ Сообщение отправлено в чат {chat_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

async def main():
    try:
        print("⌛ Подключаемся к Telegram...")
        await client.start(
            phone=phone,
            password=password,
            code_callback=lambda: input("📲 Введите код из SMS: ")
        )
        
        me = await client.get_me()
        print(f"✅ Авторизован как {me.first_name} (@{me.username})")
        
        while True:
            message = input("\nВведите сообщение (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                break
            await send_message(message)
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())