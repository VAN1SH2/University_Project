from pydantic import BaseModel

class User(BaseModel):
    id: int
    full_name: str
    phone: str
    telegram_chat_id: str
    room_id: int
    user_role: str

