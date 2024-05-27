from states.form_states import Form
from aiogram import types
import database
import asyncio
from aiogram.dispatcher import FSMContext
from utils.some_loop import some_loop
from utils.buttons import buttons
from states.activity_states import activity
from aiogram.dispatcher.filters import Text
from utils.grades import all_grades_screen
import os
from aiogram.types import BotCommand, InputFile


# В файле menu_handlers.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
# from credit.config import DONATE_LINK
import database


# dp.register_message_handler(Text(equals=["Оценки 📖", "Активность 🖊", "Донат 💸"], ignore_case=True), state=Form.mainmenu)
async def handle_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await database.get_user(user_id)
    profile_name = user[3]
    if user:
        command = message.text
        if command == "Поддержать 💸":
            await message.answer("Буду благодарен за поддержку.", reply_markup=buttons.donation_button())

            await Form.mainmenu.set()
        elif command == "Оценки 📖":
            # await handle_grades(message, state)
            await message.answer(f"Загружаю таблицу оценок пользователя: {profile_name}")

            ser_id = str(message.from_user.id)
            user = await database.get_user(user_id)  # Предполагается, что есть функция для получения пользователя из БД
            if user:
                login, password = user[1], user[2]

                result = await all_grades_screen(login, password)
                if result.startswith('Таблица с оценками успешно сохранена'):
                    file = InputFile('grades_table.png')
                    await message.answer_photo(file)
                    os.remove('grades_table.png')
                else:
                    await message.answer(result)
                    
            await Form.mainmenu.set()

        elif command == "Активность 🖊":
            is_active = user[4]
            if is_active == 1:
                await message.answer("Бот сейчас активен. Нажмите 'СТОП' для остановки активности.", reply_markup=buttons.stop())
                asyncio.create_task(some_loop(user_id))
            else:
                await message.answer("Бот сейчас не активен. Нажмите 'Старт' для начала активности.", reply_markup=buttons.start())
                await activity.waiting.set()
    else:
        await message.answer("Не удалось найти ваши данные для входа. Пожалуйста, авторизуйтесь заново.")

