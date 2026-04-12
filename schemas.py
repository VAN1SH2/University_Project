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
        from_attributes = True
#========================================
class RoomBase(BaseModel):
    room_number: int
    dormitory_number:int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True
#==========================================
class RepairRequestBase(BaseModel):
    user_id: int
    room_id: int
    category: str
    description: str
    assigned_master_id: int | None = None
    status:str
    name: str
class RepairRequestCreate(RepairRequestBase):
    pass
class RepairRequestResponse(RepairRequestBase):
    id: int

    class Config:
        from_attributes = True