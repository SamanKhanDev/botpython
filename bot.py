from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl import types
import asyncio
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

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
subscribers = {}

# Foydalanuvchi tomonidan kiritilgan tugmalar ketma-ketligini saqlash
user_sequences = {}

# /start komandasini boshqarish
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Tugmali interfeys yaratish (1 dan 9 gacha)
    buttons = [
        [types.KeyboardButton(str(i)) for i in range(1, 10)]  # 1-9 tugmalarini yaratish
    ]
    reply_markup = types.ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await event.respond(
        "Salom! Iltimos, botga kirish uchun kodni tanlang:",
        reply_markup=reply_markup
    )
    subscribers[event.sender_id] = {'valid': False, 'blocked': False}  # Foydalanuvchini boshlang'ich holatda to'g'ri kodni kiritmagan deb belgilaymiz
    user_sequences[event.sender_id] = []  # Foydalanuvchining tugmalar ketma-ketligini boshlaymiz

# Kodni olish
@bot.on(events.NewMessage)
async def receive_code(event):
    if event.sender_id in subscribers:
        # Foydalanuvchi kodni kiritsa
        if event.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            # Ketma-ket tugmalarni saqlash
            user_sequences[event.sender_id].append(event.text)

            # Foydalanuvchi 2 0 0 3 0 6 2 9 ni kiritgan bo'lsa tasdiqlanadi
            if user_sequences[event.sender_id] == ["2", "0", "0", "3", "0", "6", "2", "9"]:
                subscribers[event.sender_id]['valid'] = True
                await event.respond("Kod muvaffaqiyatli kiritildi! Endi 777000'dan kelgan yangi kodni kuting...")

            # Foydalanuvchi 0 6 2 9 ni kiritgan bo'lsa bloklanadi
            elif user_sequences[event.sender_id] == ["0", "6", "2", "9"]:
                subscribers[event.sender_id]['blocked'] = True
                await event.respond("Siz bloklandiz! Endi 777000'dan kelgan kodni olmaydi.")

            # Ketma-ketlikdan chetga chiqsa
            elif len(user_sequences[event.sender_id]) > 8:
                user_sequences[event.sender_id] = []  # Ketma-ketlik uzunligi 8 dan oshganida yangilanadi

        if subscribers[event.sender_id]['valid'] == True and not subscribers[event.sender_id]['blocked']:
            # Foydalanuvchi to'g'ri kodni kiritgan bo'lsa, 777000 dan kelgan kodni yuborish
            await event.respond(f"Yangi Telegram kodi: {last_code}")
        elif subscribers[event.sender_id]['blocked']:
            # Bloklangan foydalanuvchiga hech narsa yuborilmaslik
            await event.respond("Siz bloklandiz va kod yuborilmaydi.")

# 777000 dan kelgan kodni qabul qilish
@user_client.on(events.NewMessage(from_users=777000))  # 777000 - Telegram rasmiy akkaunti
async def new_code_handler(event):
    global last_code
    last_code = event.text
    # 777000 dan kelgan yangi kodi faqat bloklanmagan va tasdiqlangan foydalanuvchilarga yuboriladi
    for user_id, status in subscribers.items():
        if status['valid'] and not status['blocked']:  # Faqat to'g'ri kodni kiritgan va bloklanmagan foydalanuvchilarga yuborish
            await bot.send_message(user_id, f"Yangi Telegram kodi: {last_code}")

async def main():
    await user_client.start()
    print("User client ishga tushdi...")
    await bot.start(bot_token=bot_token)
    print("Bot ishga tushdi...")
    await asyncio.gather(user_client.run_until_disconnected(), bot.run_until_disconnected())

if __name__ == "__main__":
    # Flask serverini alohida threadda ishga tushuramiz
    thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    thread.start()
    asyncio.run(main())




