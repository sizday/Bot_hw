import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text, CommandStart
from state import DoneHW
import database
import sticker_id
from load_all import bot, dp

db = database.DBCommands()


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    user = await db.add_new_user()
    if user[1] == 'old':
        text = f'Вы уже зарегистрированы'
        await message.answer(text)
    else:
        text = f'Приветствую вас, {user[0].full_name}'
        await message.answer(text)


@dp.message_handler(commands=['hw'])
async def my_hw(message: types.Message):
    all_unmade_id = await db.done_unmade()
    for num, done in enumerate(all_unmade_id):
        current_hw = await db.get_hw(done.homework_id)
        text = f"<b>ДЗ</b> \t№{current_hw.id}: <u>{current_hw.title}</u>\n<b>Описание:</b> {current_hw.description}\n"
        await message.answer_document(document=current_hw.file, caption=text)
    await message.answer('Выберете номер ДЗ')
    await DoneHW.Choose.set()


@dp.message_handler(state=DoneHW.Choose)
async def choose_hw(message: types.Message, state: FSMContext):
    try:
        hw_id = int(message.text)
    except ValueError:
        await message.answer("Неверное значение, введите число")
        return
    await message.answer(f'Пришлите решение ДЗ №{hw_id}')
    hw = await db.get_hw(hw_id)
    await state.update_data(hw=hw)


@dp.message_handler(commands=['all_hw'])
async def all_hw(message: types.Message):
    all_hw = await db.list_hw()
    for num, hw in enumerate(all_hw):
        text = f"<b>ДЗ</b> \t№{hw.id}: <u>{hw.title}</u>\n<b>Описание:</b> {hw.description}\n"
        await message.answer_document(document=hw.file, caption=text)
