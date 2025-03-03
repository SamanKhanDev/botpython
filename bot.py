from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio

api_id = 1150656  # To'g'ri API ID kiriting
api_hash = "fb33d7c76f5bdaab44d5145537de31c0"  # To'g'ri API hash kiriting
bot_token = "8108266498:AAHTewUwY8lXDlfklgvnzDC_4raqp2csdHc"  # Telegram bot tokenini kiriting


# session.txt faylidan StringSession'ni o‘qish
with open("session.txt", "r") as file:
    session_string = file.read().strip()

# Foydalanuvchi sessiyasi (shaxsiy akkaunt)
user_client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Bot uchun alohida session
bot = TelegramClient('bot', api_id, api_hash)

last_code = "Hali kod olinmadi."
subscribers = set()

@user_client.on(events.NewMessage(from_users=777000))  # 777000 - Telegram rasmiy akkaunti
async def new_code_handler(event):
    global last_code
    last_code = event.text
    for user_id in subscribers:
        await bot.send_message(user_id, f"Yangi Telegram kodi: {last_code}")

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    subscribers.add(event.sender_id)
    await event.respond(f"Salom! Bot ishga tushdi.\n\nTelegramdan kelgan kod: {last_code}")

async def main():
    await user_client.start()
    print("User client ishga tushdi...")
    await bot.start(bot_token=bot_token)
    print("Bot ishga tushdi...")
    await asyncio.gather(user_client.run_until_disconnected(), bot.run_until_disconnected())

if __name__ == "__main__":
    asyncio.run(main())
