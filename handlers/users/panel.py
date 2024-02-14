from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType , InlineKeyboardMarkup, InlineKeyboardButton
import json
from data.config import ADMINS
from keyboards.inline.menu_panel import kb , cancel_kb
from loader import dp,db,bot
from states.state import *
from middlewares.subscription import load_channels_from_file
channels_file_path = 'channels.json'
def save_channels_to_file(channels):
    with open(channels_file_path, 'w') as file:
        json.dump(channels, file)

CHANNELS =load_channels_from_file()
@dp.message_handler(commands=['admin'], chat_id = ADMINS)
async def bot_echo(message: types.Message):
    await message.answer("Admin panelga xush kelibsiz.",reply_markup=kb.main())


@dp.callback_query_handler(text="send", chat_id = ADMINS)
async def Admin_send(call: types.CallbackQuery):
    await call.message.answer("Xabar turini Tanlang 👇🏻",reply_markup=kb.admin())


# TEXT xabar uchun
@dp.callback_query_handler(text="text", chat_id = ADMINS)
async def Admin_send(call: types.CallbackQuery):
    await call.message.answer("Xabar yuborish uchun matn yuboring.",reply_markup=cancel_kb)
    await send_text.text.set()

@dp.message_handler(state=send_text.text)
async def bot_echo(message: types.Message, state: FSMContext):
    all_user_id = db.select_all_users()
    for x in all_user_id:
        user_id = x[1]
        await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.finish()


# PHOTO xabar uchun
@dp.callback_query_handler(text="photo", chat_id = ADMINS)
async def Admin_send(call: types.CallbackQuery):
    await call.message.answer("Rasm yuboring.",reply_markup=cancel_kb)
    await send_phot.photo.set()

@dp.message_handler(state=send_phot.photo, content_types=ContentType.PHOTO)
async def bot_echo(message: types.Message, state: FSMContext):
    all_user_id = db.select_all_users()
    for x in all_user_id:
        user_id = x[1]
        await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.finish()


# VIDEO xabar uchun
@dp.callback_query_handler(text="video", chat_id = ADMINS)
async def Admin_send(call: types.CallbackQuery):
    await call.message.answer("Video yuboring.",reply_markup=cancel_kb)
    await send_vid.video.set()

@dp.message_handler(state=send_vid.video, content_types=ContentType.VIDEO)
async def bot_echo(message: types.Message, state: FSMContext):
    all_user_id = db.select_all_users()
    for x in all_user_id:
        user_id = x[1]
        await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.finish()


# VOICE xabar uchun
@dp.callback_query_handler(text="voice", chat_id = ADMINS)
async def Admin_send(call: types.CallbackQuery):
    await call.message.answer("Ovozli xabar yuboring.",reply_markup=cancel_kb)
    await send_voi.voice.set()

@dp.message_handler(state=send_voi.voice, content_types=ContentType.VOICE)
async def bot_echo(message: types.Message, state: FSMContext):
    all_user_id = db.select_all_users()
    for x in all_user_id:
        user_id = x[1]
        await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.finish()

#Kanal qo'shish

@dp.callback_query_handler(text="add_channel",chat_id = ADMINS)
async def add_channel(call: types.CallbackQuery):
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
            

        await call.answer(response,reply_markup=remove_inline)
    else :
        pass
    await call.message.answer("Yangi kanal qo'shish uchun kanal id sini yuboring.\nHelp: Kanal id sini olish uchun mana bu botga kanaldan istalgan postni forward qiling:\n @getmyid_bot")
        
    await add_chanel.channel.set()

@dp.message_handler(lambda msg : msg.text.startswith("-"),state=add_chanel.channel)
async def addding(message: types.Message, state: FSMContext):
    
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
    await state.finish()

@dp.callback_query_handler(text="cancel")
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer("Amal bekor qilindi")