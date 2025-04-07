from fastapi import APIRouter, HTTPException, Depends, status
from chat_room.models import Message, MessageCreate, User
from chat_room.auth_routes import get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/send", status_code=201)
async def send_message(
    msg_data: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    if not ObjectId.is_valid(msg_data.recipient_id):
        raise HTTPException(status_code=400, detail="Invalid recipient ID")

    message = Message(
        sender_id=ObjectId(current_user.id),
        recipient_id=ObjectId(msg_data.recipient_id),
        text=msg_data.text,
    )
    await message.insert()
    return {"message": "Message sent successfully"}


@router.get("/inbox")
async def get_inbox(current_user: User = Depends(get_current_user)):
    messages = await Message.find(
        Message.recipient_id == ObjectId(current_user.id)
    ).sort("-timestamp").to_list()
    return messages


@router.get("/sent")
async def get_sent_messages(current_user: User = Depends(get_current_user)):
    messages = await Message.find(
        Message.sender_id == ObjectId(current_user.id)
    ).sort("-timestamp").to_list()
    return messages
