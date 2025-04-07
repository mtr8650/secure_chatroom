import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from chat_room.models import Message, User  # ← make sure User is imported

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    database = client.chat_db
    await init_beanie(database, document_models=[Message, User])
