from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    telegram_chat_id = Column(String, nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    user_role = Column(String, nullable=False)
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, nullable=False)
    dormitory_number = Column(Integer, nullable=False)
class Repair_request(Base):
    __tablename__ = "repair_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    catecory = Column(String, nullable=False)
    description = Column(String, nullable=False)
    assigned_master_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, nullable=False)

