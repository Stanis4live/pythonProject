import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = 'my_verify_token'
ACCESS_TOKEN = 'EAAWbQZCzFS0YBOxXeltZCmb5nkp74RXOeqGJTWZAPEqSW2lkkbZADV5W6ZAZBsu8Xbthsx0BcPNpyiXZBlgPveYZBvp8HshPzFrnANEjTy3ZCmTsQvaE4alClev7X7vgTcZAmJyZAHLJFTHhAvAQPC5znFSwvsIpRalyC30FQisXSDQZBpVFmMa15yZCGj1hgYxgUFZAz0zXoMlz3xsJnZBIc6ZCdNVcZC6qjKZA8ZD'

# Замените на правильный Instagram Business Account ID
INSTAGRAM_BUSINESS_ACCOUNT_ID = '17841403722404968'  # Instagram Business Account ID
INSTAGRAM_API_VERSION = 'v21.0'

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
    url = f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/messages"
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
