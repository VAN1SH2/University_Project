import requests

# 1. Данные для отправки
url = 'http://192.168.0.131:8000/rooms/add'
data = {
    "full_name": "Ганеев Иван",
  "phone": "89501114258",
  "telegram_chat_id": "00907879768567",
  "room_id": 1,
  "user_role": "student"
}

for i in range (2, 17):
    for j in range (1, 46):
        room_number = str(i)+str(j)
        url = f'http://192.168.0.131:8000/rooms/add/{room_number}/{i}'
        response = requests.post(url)