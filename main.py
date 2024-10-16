import os

import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

app = Flask(__name__)

# Получение переменных окружения
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
IG_ID = os.getenv('IG_ID')
INSTAGRAM_API_VERSION = os.getenv('INSTAGRAM_API_VERSION')

# Добавление пустой домашней страницы
@app.route('/')
def home():
    return "Welcome to the home page!", 200

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args['hub.challenge'], 200
    return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Получено сообщение:", data)

    if 'messaging' in data['entry'][0]:
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        message_text = data['entry'][0]['messaging'][0]['message']['text']

        response_text = f"Вы отправили: {message_text}"

        send_message(sender_id, response_text)

    return "OK", 200

def send_message(sender_id, message_text):
    url = f"https://graph.instagram.com/{INSTAGRAM_API_VERSION}/{IG_ID}/messages"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'recipient': {
            'id': sender_id
        },
        'message': {
            'text': message_text
        }
    }

    response = requests.post(url, json=payload, headers=headers, verify='/etc/ssl/certs/ca-certificates.crt')
    print(f"Ответ отправлен: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=(
        '/etc/letsencrypt/live/stanis4live.su/fullchain.pem', '/etc/letsencrypt/live/stanis4live.su/privkey.pem'))

