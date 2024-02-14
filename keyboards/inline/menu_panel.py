from aiogram import types

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    def main(self):
        menu = types.InlineKeyboardMarkup(row_width=1)
        send = types.InlineKeyboardButton("♻️ Xabar Yuborish", callback_data="send")
        stat = types.InlineKeyboardButton("📊 Statistika", callback_data="stat")
        add_channel = types.InlineKeyboardButton("Kanal qo'shish",callback_data="add_channel")
        return menu.add(send,stat,add_channel)

    def menuus(self):
        menu = types.InlineKeyboardMarkup(row_width=1)
        stat = types.InlineKeyboardButton("📊 Statiska", callback_data="stat")
        return menu.add(stat)

    def admin(self):
        menu = types.InlineKeyboardMarkup(row_width=1)
        photo = types.InlineKeyboardButton("Rasmli xabar yuborish",callback_data="photo")
        video = types.InlineKeyboardButton("Video xabar yuborish", callback_data="video")
        voice = types.InlineKeyboardButton("Ovozli xabar yuborish", callback_data="voice")
        text = types.InlineKeyboardButton("Matnli xabar yuborish", callback_data="text")
        return menu.add(photo,video,voice,text)

kb = Keyboards()

cancel_kb = InlineKeyboardMarkup()
cancel_kb.add(
    InlineKeyboardButton("❌Cancel",callback_data="cancel")
)