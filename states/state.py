from aiogram.dispatcher.filters.state import State, StatesGroup

class add_chanel(StatesGroup):
    channel = State()

class send_text(StatesGroup):
    text = State()

class send_phot(StatesGroup):
    photo = State()

class send_vid(StatesGroup):
    video = State()

class send_voi(StatesGroup):
    voice = State()