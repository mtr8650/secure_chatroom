from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime

class User(Document):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # MongoDB collection name

