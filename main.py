import os
import requests
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn

# Загрузка переменных из .env
load_dotenv()

# Создаем приложение FastAPI
app = FastAPI()

# Получение переменных окружения
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
IG_ID = os.getenv('IG_ID')
INSTAGRAM_API_VERSION = os.getenv('INSTAGRAM_API_VERSION')

# Модель для входящих сообщений
class WebhookRequest(BaseModel):
    object: str
    entry: list

# Маршрут для пустой домашней страницы
@app.get("/")
async def read_root():
    return {"message": "Welcome to the home page!"}

# Маршрут для верификации вебхука
@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge
    raise HTTPException(status_code=403, detail="Verification failed")

# Маршрут для обработки сообщений от Instagram
@app.post("/webhook")
async def handle_webhook(data: WebhookRequest):
    print(f"Получено сообщение: {data}")

    for entry in data.entry:
        messaging_events = entry.get('messaging', [])
        for event in messaging_events:
            if 'message' in event:
                sender_id = event['sender']['id']
                message_text = event['message'].get('text')
                if message_text:
                    response_text = f"Вы отправили: {message_text}"
                    await send_message(sender_id, response_text)
            else:
                print("Сообщение не содержит поля 'message'")

    return {"status": "ok"}

# Функция для отправки сообщений в Instagram
async def send_message(sender_id: str, message_text: str):
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, ssl_keyfile="/etc/letsencrypt/live/stanis4live.su/privkey.pem", ssl_certfile="/etc/letsencrypt/live/stanis4live.su/fullchain.pem")
