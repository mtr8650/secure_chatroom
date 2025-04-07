from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional, Any
from passlib.context import CryptContext


# Utility for ObjectId conversion in Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v: Any) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User DB model
class User(Document):
    username: str
    email: EmailStr
    hashed_password: str

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    class Settings:
        name = "users"


# Message DB model
class Message(Document):
    sender_id: PyObjectId = Field(..., alias="sender")
    recipient_id: PyObjectId = Field(..., alias="recipient")
    text: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"


# Pydantic input models (client-facing)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class MessageCreate(BaseModel):
    recipient_id: str  # Send to another user by ID
    text: str
