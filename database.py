import asyncio
from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime, timedelta

client = MongoClient(MONGO_URI)
db = client['musicbot']
users_col = db['users']
stats_col = db['stats']

async def add_user(user_id: int, lang: str = 'ru'):
    """Foydalanuvchi qo'shish"""
    user = {'user_id': user_id, 'lang': lang, 'join_date': datetime.utcnow(), 'searches': 0}
    await users_col.replace_one({'user_id': user_id}, user, upsert=True)

async def get_user_stats():
    """Umumiy statistika"""
    total_users = await users_col.count_documents({})
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_users = await users_col.count_documents({'join_date': {'$gte': today}})
    return total_users, today_users

async def increment_search(user_id: int):
    """Qidiruv hisoblash"""
    await users_col.update_one({'user_id': user_id}, {'$inc': {'searches': 1}})

async def set_user_lang(user_id: int, lang: str):
    """Til o'zgartirish"""
    await users_col.update_one({'user_id': user_id}, {'$set': {'lang': lang}})

async def get_user_lang(user_id: int) -> str:
    """Foydalanuvchi tilini olish"""
    user = await users_col.find_one({'user_id': user_id})
    return user['lang'] if user else 'ru'

async def check_subscription(user_id: int, channel_id: int) -> bool:
    """Kanal obunasini tekshirish"""
    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Close connection
async def close_db():
    client.close()
