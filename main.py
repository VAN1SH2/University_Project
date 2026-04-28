from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, User, Room, Repair_request
from database import engine, session_local
from schemas import UserCreate, RoomBase, UserResponse, RoomCreate, RoomResponse, RepairRequestCreate, RepairRequestResponse
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
    return db_user


@app.get("/users/get/{telegram_chat_id}") 
async def get_user(telegram_chat_id: str, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.telegram_chat_id == telegram_chat_id).first()
    if db_user is None:
       raise HTTPException(status_code=404, detail="User not found")
    return(db_user)


@app.put("/users/update/{id}", response_model=UserResponse)
async def update_user(id: str, user_update: UserResponse, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.id ==int(id)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.room_id is not None:
        room = db.query(Room).fiёlter(Room.id == user_update.room_id).first()
        if room is None:
            raise HTTPException(
                status_code=400,
                detail=f"Room with id={user_update.room_id} does not exist",
            )
    db_user.full_name = user_update.full_name
    db_user.phone = user_update.phone   
    db_user.telegram_chat_id = user_update.telegram_chat_id
    db_user.room_id = user_update.room_id
    db_user.user_role = user_update.user_role
    db.commit()
    db.refresh(db_user)
    return db_user



#_____________________________________________________

# @app.post("/rooms/add/{this_room_number}/{this_dormitory_number}", response_model=RoomCreate)
# async def create_room(this_room_number: int, this_dormitory_number: int, db:Session = Depends(get_db)):
#     db_room = Room(room_number= this_room_number, dormitory_number = this_dormitory_number)
#     db.add(db_room)
#     db.commit()
#     db.refresh(db_room)

@app.get("/rooms/get/{room_number}/{dormitory_number}") 
async def get_room_id(room_number: int, dormitory_number: int, db: Session = Depends(get_db)) -> int:
    db_room = db.query(Room).filter(Room.dormitory_number == dormitory_number, Room.room_number == room_number).first()
    if db_room is None:
       raise HTTPException(status_code=404, detail="Room not found")
    return db_room.id

@app.post("/repair_request/add", response_model=RepairRequestResponse)
async def create_repair_request(repair_request: RepairRequestCreate, db: Session = Depends(get_db)) -> Repair_request:
    if repair_request.room_id is not None:
        room = db.query(Room).filter(Room.id == repair_request.room_id).first()
        if room is None:
            raise HTTPException(
                status_code=400,
                detail=f"Room with id={repair_request.room_id} does not exist",
            )
    if repair_request.user_id is not None:
        user = db.query(User).filter(User.id == repair_request.user_id).first()
        if user is None:
            raise HTTPException(
                status_code=400,
                detail=f"User with id={repair_request.user_id} does not exist",
            )
    if repair_request.assigned_master_id is not None:
        assigned_master = db.query(User).filter(User.id == repair_request.assigned_master_id).first()
        if assigned_master is None:
            raise HTTPException(
                status_code=400,
                detail=f"User with id={repair_request.assigned_master_id} does not exist",
            )

    db_repair_request = Repair_request (user_id = repair_request.user_id, room_id = repair_request.room_id, 
                    category = repair_request.category, description = repair_request.description,
                    assigned_master_id = repair_request.assigned_master_id,
                    status = repair_request.status, name = repair_request.name)
    db.add(db_repair_request)

    db.commit()
    db.refresh(db_repair_request)
    return db_repair_request

# ------------------------------------------------------------------------------
@app.get("/repair_requests/get")
async def get_repair_requests(db: Session = Depends(get_db)) -> list[RepairRequestResponse]:
    db_repair_requests = db.query(Repair_request).filter(Repair_request.status == "new").all()
    return db_repair_requests

@app.patch("/repair_requests/update_status/{id}/{status_update}") 
async def update_repair_request(id: int, status_update: str, db: Session = Depends(get_db)) -> RepairRequestResponse:
    db_repair_request = db.query(Repair_request).filter(Repair_request.id == id).first()
    if db_repair_request is None:
       raise HTTPException(status_code=404, detail="Repair request not found")
    db_repair_request.status = status_update
    db.commit()
    db.refresh(db_repair_request)
    return db_repair_request

