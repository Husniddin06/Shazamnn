from aiogram_translation import FSTranslationManager

translations = FSTranslationManager(locales_dir="locales")  # locales papkasini yarating

# Agar papka yo'q bo'lsa, ichida locales/uz.json, locales/ru.json, locales/en.json yarating

UZ_TEXTS = {
    "welcome": """
👋 Salom!
Musiqa topishga yordam beraman 🎶, quyidagilardan birini yuboring:

🎵 Qo'shiq nomi yoki ijrochi
🔤 Qo'shiq matni
🎙 Musiqa bilan ovozli xabar
📹 Musiqa bilan video
🔊 Audio yozuv
🎥 Musiqa bilan video xabar
🔗 Instagram, TikTok, YouTube havolasi

🕺 Zavqlaning!
    """,
    "searching": "🔄 Qidirilmoqda...",
    "downloading": "📥 Yuklanmoqda...",
    "no_results": "❌ Hech narsa topilmadi!",
    "admin_panel": "👨‍💼 Admin panel:\n👥 Foydalanuvchilar: {users}\n📊 Bugun: {today}",
    "lang_changed": "✅ Til o'zgartirildi: {lang}",
    "subscribe_first": "📢 Avval kanalga obuna bo'ling!"
}

RU_TEXTS = {
    "welcome": """
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
    """,
    "searching": "🔄 Ищу...",
    "downloading": "📥 Скачиваю...",
    "no_results": "❌ Ничего не найдено!",
    "admin_panel": "👨‍💼 Админ панель:\n👥 Пользователей: {users}\n📊 Сегодня: {today}",
    "lang_changed": "✅ Язык изменен: {lang}",
    "subscribe_first": "📢 Сначала подпишись на канал!"
}

EN_TEXTS = {
    "welcome": """
👋 Hi!
I'll help find music 🎶, send me one of these:

🎵 Song name or artist
🔤 Lyrics snippet
🎙 Voice message with music
📹 Video with music
🔊 Audio recording
🎥 Video message with music
🔗 Link to Instagram, TikTok, YouTube video

🕺 Enjoy!
    """,
    "searching": "🔄 Searching...",
    "downloading": "📥 Downloading...",
    "no_results": "❌ No results found!",
    "admin_panel": "👨‍💼 Admin panel:\n👥 Users: {users}\n📊 Today: {today}",
    "lang_changed": "✅ Language changed: {lang}",
    "subscribe_first": "📢 Subscribe to channel first!"
}
