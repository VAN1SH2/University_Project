from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, User, Room, Repair_request
from database import engine, session_local
from schemas import UserCreate, RoomBase
from sqlalchemy.exc import IntegrityError

app = FastAPI()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/add", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    if user.room_id is not None:
        room = db.query(Room).filter(Room.id == user.room_id).first()
        if room is None:
            raise HTTPException(
                status_code=400,
                detail=f"Room with id={user.room_id} does not exist",
            )

    db_user = User (full_name = user.full_name, phone = user.phone, 
                    telegram_chat_id = user.telegram_chat_id, room_id = user.room_id,
                    user_role = user.user_role)
    db.add(db_user)

    db.commit()
    db.refresh(db_user)
    # except IntegrityError as exc:
    #     db.rollback()
    return db_user

@app.get("/users/get") 

async def get_user(tg_id: str, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.telegram_chat_id == tg_id).first()
    if db_user is None:
       raise HTTPException(status_code=404, detail="User not found")
    return(db_user)
