import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "7810588142:AAGBNgggP3KTpN1lQ5MCQRZx7WHfc-fk9rA")
ADMIN_ID = 1999635628
PRIVATE_CHANNEL_ID = -1003939199104  # Kanal ID (minus bilan)
SUB_CHANNEL_ID = -1001234567890  # Obuna kanaling ID sini keyin o'zgartir

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/musicbot")  # MongoDB Atlas

# Tilllar
LANGUAGES = {
    'uz': {'code': 'uz', 'name': '🇺🇿 O\'zbek'},
    'ru': {'code': 'ru', 'name': '🇷🇺 Русский'},
    'en': {'code': 'en', 'name': '🇺🇸 English'}
}

# Start matni (rus misol, keyin tarjima)
WELCOME_RU = """
👋 Привет!
Я помогу найти музыку 🎶, отправь мне что-то из этого:

🎵 Название песни или исполнителя
🔤 Слова из песни
🎙 Голосовое сообщение с музыкой
📹 Видео с музыкой
🔊 Аудиозапись
🎥 Видеосообщение с музыкой
🔗 Ссылку на видео в Instagram, Tik-Tok, YouTube и другие сайты

🕺 Наслаждайся!
"""

# Download sozlamalari
YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'postprocessor_args': ['-vn'],
    'noplaylist': True,
    'quiet': True,
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
