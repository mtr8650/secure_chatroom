import pytest
from httpx import AsyncClient
from fastapi import status
from httpx._transports.asgi import ASGITransport

from chat_room.main import app, app_init  # ✅ Import app_init from main.py
from chat_room.models import User, Message  # ✅ Also import Message


@pytest.mark.asyncio
async def test_register_and_login_and_send_message():
    # ✅ Manually call FastAPI's startup logic
    await app_init()

    # ✅ Clear the DB collections before running the test
    await User.find_all().delete()
    await Message.find_all().delete()

    # ✅ Use ASGITransport for test client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Register user1 (Alice)
        user1_data = {"username": "alice", "email": "alice@example.com", "password": "secret"}
        res = await ac.post("/auth/register", json=user1_data)
        print("REGISTER RESPONSE:", res.status_code, res.json())
        assert res.status_code == status.HTTP_200_OK

        # Register user2 (Bob)
        user2_data = {"username": "bob", "email": "bob@example.com", "password": "secret"}
        res = await ac.post("/auth/register", json=user2_data)
        assert res.status_code == status.HTTP_200_OK

        # Login as Alice
        login_res = await ac.post("/auth/login", json={"email": user1_data["email"], "password": user1_data["password"]})
        assert login_res.status_code == status.HTTP_200_OK
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Fetch Bob’s ID
        bob = await User.find_one(User.email == user2_data["email"])
        assert bob is not None

        # Send message from Alice to Bob
        message = {"recipient_id": str(bob.id), "text": "Hey Bob!"}
        send_res = await ac.post("/send", json=message, headers=headers)
        assert send_res.status_code == status.HTTP_200_OK

        # Login as Bob and check inbox
        login_res = await ac.post("/auth/login", json={"email": user2_data["email"], "password": user2_data["password"]})
        assert login_res.status_code == status.HTTP_200_OK
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        inbox_res = await ac.get("/inbox", headers=headers)
        assert inbox_res.status_code == status.HTTP_200_OK
        inbox = inbox_res.json()
        assert any("Hey Bob!" in msg["text"] for msg in inbox)

