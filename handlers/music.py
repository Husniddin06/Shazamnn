import os
import asyncio
import yt_dlp
from pathlib import Path

from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import CommandStart, Command

from config import (
    YDL_OPTS,
    PRIVATE_CHANNEL_ID,
    SUB_CHANNEL_ID,
    ADMIN_ID,
    LANGUAGES,
)
from translations import UZ_TEXTS, RU_TEXTS, EN_TEXTS
from database import (
    add_user,
    increment_search,
    get_user_lang,
    set_user_lang,
)

router = Router()

# downloads papkasini yaratamiz
Path("downloads").mkdir(exist_ok=True)


def get_text(lang: str, key: str, **kwargs) -> str:
    if lang == "uz":
        d = UZ_TEXTS
    elif lang == "en":
        d = EN_TEXTS
    else:
        d = RU_TEXTS
    text = d.get(key, "")
    if kwargs:
        return text.format(**kwargs)
    return text


async def download_with_ytdlp(url: str) -> tuple[str, str]:
    """
    yt-dlp bilan audio yuklash.
    Return: (file_path, title)
    """
    loop = asyncio.get_running_loop()

    def _download():
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Unknown")
            file_path = ydl.prepare_filename(info)
            base, _ = os.path.splitext(file_path)
            mp3_path = base + ".mp3"
            return mp3_path, title

    file_path, title = await loop.run_in_executor(None, _download)
    return file_path, title


async def send_to_private_channel(bot, file_path: str, title: str):
    """
    Faylni private kanalga yuklash va file_id qaytarish.
    """
    with open(file_path, "rb") as f:
        msg = await bot.send_audio(
            chat_id=PRIVATE_CHANNEL_ID,
            audio=f,
            title=title,
        )
    return msg.audio.file_id


async def ensure_subscription(bot, user_id: int, lang: str) -> bool:
    """
    Foydalanuvchi SUB_CHANNEL_ID ga obuna bo'lganmi – tekshiradi.
    Obuna bo'lmasa, kanalga link bilan xabar yuboradi.
    """
    if SUB_CHANNEL_ID == 0:
        return True  # obuna o'chirilgan

    try:
        member = await bot.get_chat_member(SUB_CHANNEL_ID, user_id)
        if member.status in ("member", "administrator", "creator"):
            return True
    except Exception:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanal",
                    url=f"https://t.me/c/{str(SUB_CHANNEL_ID)[4:]}",  # private/ochiqga qarab o'zgartirasan
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Tekshirish",
                    callback_data="check_sub",
                )
            ],
        ]
    )
    await bot.send_message(
        chat_id=user_id,
        text=get_text(lang, "subscribe_first"),
        reply_markup=kb,
    )
    return False


@router.message(CommandStart())
async def cmd_start(message: Message, bot):
    tg_lang = (message.from_user.language_code or "ru").lower()
    if tg_lang.startswith("uz"):
        lang = "uz"
    elif tg_lang.startswith("en"):
        lang = "en"
    else:
        lang = "ru"

    await add_user(message.from_user.id, lang)

    text = get_text(lang, "welcome")
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            ]
        ]
    )
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.startswith("lang_"))
async def cb_change_lang(callback, bot):
    lang = callback.data.split("_", 1)[1]
    if lang not in LANGUAGES:
        lang = "ru"

    await set_user_lang(callback.from_user.id, lang)
    await callback.answer(get_text(lang, "lang_changed", lang=LANGUAGES[lang]["name"]), show_alert=True)
    await callback.message.edit_text(get_text(lang, "welcome"))


@router.message(Command("lang"))
async def cmd_lang(message: Message, bot):
    lang = await get_user_lang(message.from_user.id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            ]
        ]
    )
    await message.answer(get_text(lang, "lang_changed", lang=LANGUAGES[lang]["name"]), reply_markup=kb)


@router.message(F.text.regexp(r"https?://"))
async def handle_link(message: Message, bot):
    """
    Instagram / TikTok / YouTube / VK linklari.
    """
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    if not await ensure_subscription(bot, user_id, lang):
        return

    await increment_search(user_id)
    url = message.text.strip()

    status_msg = await message.answer(get_text(lang, "downloading"))

    try:
        file_path, title = await download_with_ytdlp(url)
    except Exception as e:
        await status_msg.edit_text(get_text(lang, "no_results"))
        return

    try:
        file_id = await send_to_private_channel(bot, file_path, title)
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=file_id,
            title=title,
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        await status_msg.delete()


@router.message(F.text & ~F.text.regexp(r"https?://"))
async def handle_text_search(message: Message, bot):
    """
    Qo'shiq nomi / artist matn orqali qidirish.
    yt-dlp qidiruvdan ham ishlaydi: "ytsearch1: ..." formatida.
    """
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    if not await ensure_subscription(bot, user_id, lang):
        return

    await increment_search(user_id)
    query = message.text.strip()

    status_msg = await message.answer(get_text(lang, "searching"))

    search_url = f"ytsearch1:{query}"

    try:
        file_path, title = await download_with_ytdlp(search_url)
    except Exception:
        await status_msg.edit_text(get_text(lang, "no_results"))
        return

    try:
        file_id = await send_to_private_channel(bot, file_path, title)
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=file_id,
            title=title,
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        await status_msg.delete()
