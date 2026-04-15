import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database import close_db
from handlers_music import router as music_router

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Routerlarni qo'shish
dp.include_router(music_router)

# Admin handlerlar
@dp.message(lambda message: message.from_user.id == config.ADMIN_ID and message.text == "/admin")
async def admin_panel(message):
    total_users, today_users = await get_user_stats()
    lang = "ru"  # Admin uchun rus
    
    text = get_text(lang, "admin_panel", users=total_users, today=today_users)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📤 Reklama yubor", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🔄 Restart", callback_data="admin_restart")],
        [InlineKeyboardButton("❌ Yopish", callback_data="admin_close")]
    ])
    await message.answer(text, reply_markup=kb)

@dp.message(lambda message: message.from_user.id == config.ADMIN_ID and message.text == "/stats")
async def admin_stats(message):
    total_users, today_users = await get_user_stats()
    await message.answer(f"👥 Jami: {total_users}\n📊 Bugun: {today_users}")

@dp.message(lambda message: message.from_user.id == config.ADMIN_ID and message.text.startswith("/broadcast"))
async def admin_broadcast(message):
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        return await message.reply("Matn yuboring!")
    
    users = users_col.find()
    sent = 0
    for user in users:
        try:
            await bot.send_message(user['user_id'], text)
            sent += 1
            await asyncio.sleep(0.05)  # Rate limit
        except:
            continue
    
    await message.reply(f"✅ {sent} taga yuborildi!")

async def main():
    # FFmpeg tekshirish (Replit uchun)
    if not os.path.exists("/usr/bin/ffmpeg"):
        os.system("apt update && apt install -y ffmpeg")
    
    print("🤖 Music Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.run(close_db())
