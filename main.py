import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = 'my_verify_token'
ACCESS_TOKEN = 'EAAWbQZCzFS0YBOxU2QmcSa7CbCnfZBrDhyUgFvqxpSrwRWHxqV0nZCfd4ZB9TaQhGVKZC8AkhZC8bay7i3D2FZAZCoAA8Gtfio3Q4ZBqz3JDfplFutqAR8brywrb5EPWMU1eeExdchaPZCjkTrJit6Yol9yR3nZBfTDl9mZAitaulrqygUvidGlAC8zeiQezv82BXZBnxk7sbX8Xl4k3s1ZAWHMAZDZD'

INSTAGRAM_APP_ID = '27006061152371078'
INSTAGRAM_API_VERSION = 'v21.0'

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
    url = f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}/{INSTAGRAM_APP_ID}/messages"
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

    response = requests.post(url, json=payload, headers=headers, verify=False)
    print(f"Ответ отправлен: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=(
        '/etc/letsencrypt/live/stanis4live.su/fullchain.pem', '/etc/letsencrypt/live/stanis4live.su/privkey.pem'))

