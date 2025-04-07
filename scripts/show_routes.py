from chat_room.main import app

for route in app.routes:
    print(f"{route.path} -> {route.name}")
