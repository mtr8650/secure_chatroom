import asyncio
from chat_room.email_utils import send_email_notification

async def main():
    await send_email_notification(
        to_email="mohamadtaha8650@gmail.com",
        subject="🚀 Email Test from Chatroom",
        body="If you're seeing this, email sending works!"
    )

asyncio.run(main())
