import json
from aiogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from loader import dp



channels_file_path = 'channels.json'


def load_channels_from_file():
    try:
        with open(channels_file_path, 'r') as file:
            channels = json.load(file)
            return channels
    except FileNotFoundError:
        return []

# Sizning loyiha bo'yicha kanallar ro'yxati
CHANNELS = load_channels_from_file()



inline_keyboards = InlineKeyboardMarkup()

async def add_in_kybrd(i):
    global inline_keyboards
    i = await dp.bot.get_chat(i)
    i_title = i.title
    i_username = i.username
    
    btn = InlineKeyboardButton(text=i_title,url=f"https://t.me/{i_username}")
    inline_keyboards.add(btn)
    return inline_keyboards


async def check_subscription(user_id):
    const = True
    if CHANNELS:
        for i in CHANNELS:
            chat_member = await dp.bot.get_chat_member(i,user_id)
            if chat_member.status == "creator" or chat_member.status == "adminstrator" or chat_member.status == "member":
                pass
            else :
                req = await add_in_kybrd(i)
                await message.answer(f"Siz kannallarga obuna emassiz. Obuna bo'ling",reply_markup=inline_keyboards)
                const =  False
        inline_keyboards.inline_keyboard = []
    else :
        const = True
    return const
    