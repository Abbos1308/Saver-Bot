import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '6951319877:AAEM0i-DPZUiPOrnAb1qQ3nTTPlXaxHLGTI'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Handler for /start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm your bot. Click the button below to see what I can do.", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Click me!", callback_data="click_me")))

# Handler for inline button callback
@dp.callback_query_handler(lambda query: query.data == 'click_me')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "You clicked the button!")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)