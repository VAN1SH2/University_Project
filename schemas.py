from pydantic import BaseModel

class UserBase(BaseModel):
    full_name: str
    phone: str | None = None
    telegram_chat_id: str | None = None
    room_id: int
    user_role: str| None = None

class UserCreate(UserBase):
    pass

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True
#========================================
class RoomBase(BaseModel):
    room_number: int
    dormitory_number:int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    class Config:
        orm_mode = True
