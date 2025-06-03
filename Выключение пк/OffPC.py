from flask import Flask, request
import os

app = Flask(__name__)

# Простой ключ авторизации (для безопасности)
AUTH_KEY = 'my-secret-key'

@app.route('/shutdown', methods=['GET', 'POST'])  # Теперь поддерживает и GET, и POST
def shutdown():
    key = request.args.get('key')
    if key != AUTH_KEY:
        return 'Unauthorized', 403
    # Для Windows
    os.system('shutdown /s /t 0')  
    # Для Linux можно раскомментировать следующую строку
    # os.system('sudo shutdown now')  
    return 'Shutting down...'
    print('Shutting down...')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Примечание: для Linux может потребоваться запускать скрипт с правами суперпользователя
# или настроить sudo без пароля для команды shutdown.   