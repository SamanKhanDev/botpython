from telethon.sync import TelegramClient
from telethon.sessions import StringSession


api_id = 1150656  # API ID to'g'ri yozildi
api_hash = "fb33d7c76f5bdaab44d5145537de31c0"  

with TelegramClient(StringSession(), api_id, api_hash) as client:
    client.start()  # Telefon raqamingizni va kodni kiritasiz
    session_str = client.session.save()
    print("Your session string:")
    print(session_str)
    
    # Sessiyani faylga yozish
    with open("session.txt", "w") as file:
        file.write(session_str)
