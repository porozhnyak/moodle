from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import asyncio
from states.form_states import Form
from utils.buttons import buttons
import database

# @dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):

    await state.finish()

    user_id = message.from_user.id
    user = await database.get_user(user_id)

    if user:
        login, password, profile_name, is_active = user[1], user[2], user[3], user[4]
        await message.answer(f"Привет! Выбери профиль: ", reply_markup=buttons.authorization(profile_name))
        # код в разработке
    else:
        await message.answer("Привет! Я бот для площадки moodle.")
        await asyncio.sleep(1)
        await message.answer("Что бы начать работу давай авторизуемся.")
        await asyncio.sleep(1)
        await message.answer("Введи свой логин от Moodle. ")
        await Form.login.set()