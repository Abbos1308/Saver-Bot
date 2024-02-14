import asyncio
from pytube import YouTube
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import time
import requests
from loader import dp
from data.config import ADMINS
from keyboards.inline.keyboards import keyboards
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup,InlineKeyboardButton
import json
from insta import Downloads




print(ADMINS)
print(type(ADMINS))
# Fayl nomi
channels_file_path = 'channels.json'
def save_channels_to_file(channels):
    with open(channels_file_path, 'w') as file:
        json.dump(channels, file)

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


async def check_subscription(message: types.Message):
    user_id = message.from_user.id
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
    
            #await create_in_kybrd()

def load_user_ids():
    try:
        with open('user_ids.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
user_ids = load_user_ids()
@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    my_kb = InlineKeyboardMarkup()
    my_kb.add(InlineKeyboardButton("salom", callback_data="salom"))
    await message.answer("🤖Bu bot orqali quyidagilarni yuklab olishingiz mumkin: \n• Instagram - (stories/post/reels) [Tez kunda]\n• TikTok - (video/photo)\n• YouTube - (video)\n\nShazam: [Tez kunda]\n• Qo'shiq nomi yoki ijrochi ismi\n• Video \n• Audio\n\n😉Maksimal yuklash hajmi - 400mb\n🤖 @full_downloaderr_bot\n /help - Yordam uchunffff", reply_markup=my_kb)
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
        
        # Saqlangan user id larni json faylga yozamiz
        with open('user_ids.json', 'w') as f:
            json.dump(user_ids, f)
    a = await check_subscription(message)

@dp.callback_query_handler(text="salom")
async def test(call: types.CallbackQuery):
    print("hdhdjdjjs")
    await call.message.answer("Everything ok...")


@dp.message_handler(commands=["help"])
async def help(message:types.Message):
    await message.answer("/start  - Botni ishga tushurish\n/help - Yordam\n Botdan foydalanish uchun shunchaki kerakli havolani yuboring")


# "/video" buyrug'iga javob berish funksiyasi
@dp.message_handler(lambda message: message.text.startswith("https://you"))
async def send_video(message: types.Message):
    if await check_subscription(message):
        await message.answer("Loading...")
        start_time = time.time()  # Yuklab olish boshlanish vaqti
        video_url = message.text
        try:
            yt = YouTube(video_url)
        
            filename = "video" + '.mp4'
            loop = asyncio.get_event_loop()
            # Quyidagi o'lchovlar tez yuklash uchun ishlatiladi
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            
            video_path = await loop.run_in_executor(None, stream.download)
            await message.answer("Uploading to telegram...")
            with open(video_path, 'rb') as video:
                await dp.bot.send_video(message.chat.id, video, caption=yt.title)
            end_time = time.time()  # Yuklab olish tugash vaqti
            elapsed_time = (end_time - start_time)/60  # Yuklab olish vaqti
        
            await message.answer(f"video {elapsed_time:.2f} minutda yuklandi.")
        except:
            await message.reply("Yaroqsiz link. Tekshirib qayta jo'nating")
        try:
            os.remove(video_path)
        except:
            pass

@dp.message_handler(lambda message: message.text.startswith("https://vm.tiktok.com") or message.text.startswith("https://vt.tiktok.com"))


async def send_tikvideo(message: types.Message):
    if await check_subscription(message):
        url = "https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/vid/index"
        video_url = message.text
        querystring = {"url": video_url}
        
        headers = {
            "X-RapidAPI-Key": "913d2822eemsh19cdbd1ccfa70ccp1098c9jsn42392168a2a7",
            "X-RapidAPI-Host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
        }
        try:
            await message.answer("Loading...")
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Xato bo'lganida HTTPError chiqaradi
            data = response.json()
            if data['post_type'] == "video_post":
                await message.answer("Uploading to telegram")
                await message.answer_video(data["video"][0])
            else :
                await message.answer_photo(data["photo"][0])
        except :
            await message.answer("Nimadir xato ketdi.Qayta urinib ko'ring.")

@dp.message_handler(lambda message: message.text.startswith("https://www.insta") or message.text.startswith("https://insta"))
async def insta(message: types.Message):
    await message.answer("Iltimos Kuting...")
    from insta import Downloads
    #loop = asyncio.get_event_loop()
    #res = loop.run_until_complete(Downloads.instagram(message.text))
    res = await Downloads.instagram(message.text)
    
    
    







@dp.message_handler(commands=['panel'])
async def admin_panel(message: types.Message):
    print("panel")
    user_id = str(message.from_user.id)
    if user_id in ADMINS:
        await message.answer("Admin panelga xush kelibsiz! Nima xizmat?",reply_markup=keyboards)

@dp.message_handler(lambda message: message.text.lower() == "chiqish")
async def exit_from_panel(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Botdan foydalanishingiz mumkin!",reply_markup=ReplyKeyboardRemove())
@dp.message_handler(lambda message: message.text == "Kanallar")
async def add_channel(message: types.Message):
    
    if str(message.from_user.id) in ADMINS:
        print("h")
        if CHANNELS:
            remove_inline = InlineKeyboardMarkup()
            chanels = []
            for channel in CHANNELS:
                chanel_info = await dp.bot.get_chat(channel)
                chanel = {
                    "id":channel,
                    "title": chanel_info.title,
                    "username": chanel_info.username,
                }
                chanels.append(chanel)
            response = "Kanallar ro'yxati:\n\n"
            for i in  chanels:
                response += f"{i['title']}\n@{i['username']}\n\n"
                btn = InlineKeyboardButton(text=f"{i['title']}'ni olib tashlash",callback_data=f"{i['id']},remove")
                remove_inline.add(btn)
            

            await message.answer(response,reply_markup=remove_inline)
        else :
            pass
        await message.answer("Yangi kanal qo'shish uchun kanal id sini yuboring.\nHelp: Kanal id sini olish uchun mana bu botga kanaldan istalgan postni forward qiling:\n @getmyid_bot")
        
@dp.message_handler(lambda message: message.text.startswith("-"))
async def adding(message: types.Message):
    if 2<5:
        if str(message.from_user.id) in ADMINS:
            try :
                channel = await dp.bot.get_chat(message.text)
                global CHANNELS
                if message.text in CHANNELS:
                    await message.answer("Bu kanal qo'shilgan")
                else:
                    CHANNELS.append(message.text)
                    save_channels_to_file(CHANNELS)
                    await message.answer("Kanal qo'shildi")
            except:
                await message.answer("Bizni kanalga admin qiling")
@dp.callback_query_handler(lambda call: "remove" in call.data)
async def remove_channel(call:types.CallbackQuery):
    if 2<6:
        if str(call.from_user.id) in ADMINS:
            my_list = call.data.split(",")
            global CHANNELS
            CHANNELS.remove(my_list[0])
            await call.answer("Kanal olib tashlandi")
            
@dp.message_handler(lambda message: message.text=="Adminlar")
async def admins(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        response = "Adminlar:\n"
        for admin in ADMINS:
            admin = await dp.bot.get_chat(admin)
            response += f"{admin.full_name}\n@{admin.username}\n\n"
        await message.answer(response)
        
        
@dp.message_handler(lambda message: message.text=="Statistika")
async def statistic(message:types.Message):
    if str(message.from_user.id) in ADMINS:
        users = load_user_ids()
        users_num = len(users)
        data = f"Foydalanuvchilar soni : {users_num}"
        await message.answer(data)
        
@dp.message_handler(lambda message: message.text=="Reklama berish")
async def send_ad(message:types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Yaxshi. Reklama postini yuboring")

        @dp.message_handler()
        async def forward_message(message: types.Message):
            msg = message.text
            users = load_user_ids()
            for id in users:
                await dp.bot.send_message(id,msg)
    
        # Reply to the sender
            await message.reply("Xabaringiz yuborildi!")

if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True)