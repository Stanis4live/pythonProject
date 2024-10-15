import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = 'my_verify_token'  # Ваш токен для верификации
ACCESS_TOKEN = 'EAAWbQZCzFS0YBOxXeltZCmb5nkp74RXOeqGJTWZAPEqSW2lkkbZADV5W6ZAZBsu8Xbthsx0BcPNpyiXZBlgPveYZBvp8HshPzFrnANEjTy3ZCmTsQvaE4alClev7X7vgTcZAmJyZAHLJFTHhAvAQPC5znFSwvsIpRalyC30FQisXSDQZBpVFmMa15yZCGj1hgYxgUFZAz0zXoMlz3xsJnZBIc6ZCdNVcZC6qjKZA8ZD'  # Замените на маркер доступа, сгенерированный для вашей страницы

# Данные приложения Instagram
INSTAGRAM_APP_ID = '27006061152371078'  # ID приложения
INSTAGRAM_APP_SECRET = '0b0fe9aea801f3c4cae3e54615826af9'  # Секрет приложения (Не оставляйте его открытым в реальных приложениях)
INSTAGRAM_API_VERSION = 'v21.0'


# Эндпоинт для верификации Webhook от Instagram
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args['hub.challenge'], 200
    return 'Verification failed', 403


# Эндпоинт для обработки уведомлений от Instagram
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Получено сообщение:", data)

    # Если получено сообщение
    if 'messaging' in data['entry'][0]:
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']  # ID отправителя
        message_text = data['entry'][0]['messaging'][0]['message']['text']  # Текст сообщения

        # Формируем ответное сообщение
        response_text = f"Вы отправили: {message_text}"

        # Отправляем ответ через Instagram API
        send_message(sender_id, response_text)

    return "OK", 200


def send_message(sender_id, message_text):
    url = f"https://graph.instagram.com/{INSTAGRAM_API_VERSION}/me/messages"
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

    response = requests.post(url, json=payload, headers=headers)
    print(f"Ответ отправлен: {response.status_code}, {response.text}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=(
    '/etc/letsencrypt/live/stanis4live.su/fullchain.pem', '/etc/letsencrypt/live/stanis4live.su/privkey.pem'))
