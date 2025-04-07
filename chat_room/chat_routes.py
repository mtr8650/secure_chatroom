from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from chat_room.models import Message, MessageCreate, User
from beanie import PydanticObjectId
from datetime import datetime, timezone
import os

from chat_room.email_utils import send_email_notification  # ✅ Import email utility


router = APIRouter(tags=["chat"])

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ✅ Dependency to get current user from JWT
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


# ✅ Message sending with email alert
@router.post("/send")
async def send_message(
    msg: MessageCreate, current_user: User = Depends(get_current_user)
):
    # Find the recipient user
    recipient = await User.get(PydanticObjectId(msg.recipient_id))
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Create and insert the message
    message = Message(
        sender_id=str(current_user.id),
        recipient_id=msg.recipient_id,
        text=msg.text,
        timestamp=datetime.now(timezone.utc),
    )
    await message.insert()

    # ✅ Send email notification
    await send_email_notification(
        to_email=recipient.email,
        subject="📨 New Message Received",
        body=f"You have a new message from {current_user.username}: {msg.text}"
    )

    return {"msg": "Message sent successfully"}


# ✅ Get inbox for logged-in user
@router.get("/inbox")
async def get_inbox(current_user: User = Depends(get_current_user)):
    messages = await Message.find(Message.recipient_id == str(current_user.id)).sort("-timestamp").to_list()
    return messages
