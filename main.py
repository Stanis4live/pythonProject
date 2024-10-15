from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = 'my_verify_token'  # Это произвольная строка, которую ты указываешь для верификации

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
    # Обработка данных webhook (например, сообщений)
    print("Получено сообщение:", data)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)
