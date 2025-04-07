# main.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from chat_room.models import User, Message
from chat_room.auth_routes import router as auth_router
from chat_room.chat_routes import router as chat_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    db = client["test_db"]  # ✅ Make sure this is not using .get_default_database()
    await init_beanie(database=db, document_models=[User, Message])

# ✅ REGISTER ROUTES IMMEDIATELY AFTER APP IS CREATED
app.include_router(auth_router  )
app.include_router(chat_router, tags=["chat"])
