# chat_room/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from chat_room.models import User, Message

async def init_db():
    client = AsyncIOMotorClient("mongodb://mongo:27017")  # or localhost if not using Docker
    db = client.chat_db
    await init_beanie(database=db, document_models=[User, Message])
