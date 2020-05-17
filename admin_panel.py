from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from state import NewHW
import database
from config import admin_id
from load_all import dp, bot
from database import HW

db = database.DBCommands()


@dp.message_handler(user_id=admin_id, commands=["count_user"])
async def count_user(message: types.Message):
    chat_id = message.from_user.id
    count_users = await db.count_users()
    text = f'В базе {count_users} пользователей'
    await bot.send_message(chat_id, text)


@dp.message_handler(user_id=admin_id, commands=["count_hw"])
async def count_user(message: types.Message):
    chat_id = message.from_user.id
    count_hw = await db.count_hw()
    text = f'В базе {count_hw} ДЗ'
    await bot.send_message(chat_id, text)


@dp.message_handler(user_id=admin_id, commands=["cancel"], state=NewHW)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили добавление ДЗ")
    await state.reset_state()


@dp.message_handler(user_id=admin_id, commands=["add_hw"])
async def add_item(message: types.Message):
    await message.answer("Введите название ДЗ или нажмите /cancel")
    await NewHW.Title.set()


@dp.message_handler(user_id=admin_id, state=NewHW.Title)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    hw = HW()
    hw.title = name

    await message.answer(f"Название: {name}\nПришлите мне описание или нажмите /cancel")
    await NewHW.Description.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Description)
async def add_photo(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.description = description

    await message.answer(f"Название: {hw.title}\nОписание: {description}")

    await NewHW.Confirm.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Confirm)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    hw: HW = data.get("hw")
    await hw.create()
    await message.answer('ДЗ успешно добавлено')
    await state.reset_state()
