import pytest
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.mark.asyncio
async def test_mongo_connection():
    connection_string = "mongodb://localhost:27017"

    print(f"Connecting to Mongo at: {connection_string}")
    
    client = AsyncIOMotorClient(connection_string)
    db = client.chat_db  # Adjust to your actual DB name
    messages = await db.message.find().to_list(length=10)

    if messages:
        for msg in messages:
            print(msg)
        assert True
    else:
        print("❌ No messages found!")
        assert False  # Fail the test if nothing is found
