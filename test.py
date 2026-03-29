import requests

# 1. Данные для отправки
url = 'http://192.168.0.131:8000/users/add'
data = {
    "full_name": "Ганеев Иван",
  "phone": "89501114258",
  "telegram_chat_id": "00907879768567",
  "room_id": 1,
  "user_role": "student"
}


response = requests.post(url, json=data)

if response.status_code == 200:
    print("Успех:", response.json()) # Получение JSON-ответа [4]
else:
    print("Ошибка:", response.status_code)