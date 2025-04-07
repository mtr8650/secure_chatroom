from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from chat_room.models import Message, MessageCreate, User
from beanie import PydanticObjectId
from datetime import datetime, timezone
import os

router = APIRouter(tags=["chat"])

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await User.get(PydanticObjectId(user_id))
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/send")
async def send_message(
    msg: MessageCreate, current_user: User = Depends(get_current_user)
):
    message = Message(
        sender_id=str(current_user.id),  # Convert to str
        recipient_id=msg.recipient_id,   # Already a str
        text=msg.text,
        timestamp=datetime.now(timezone.utc),  # timezone-aware
    )
    await message.insert()
    return {"msg": "Message sent successfully"}


@router.get("/inbox")
async def get_inbox(current_user: User = Depends(get_current_user)):
    messages = await Message.find(Message.recipient_id == str(current_user.id)).sort("-timestamp").to_list()
    return messages
    
