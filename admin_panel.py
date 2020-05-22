from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from state import NewHW
import database
from config import admin_id
from load_all import dp, bot
from database import HW, User, Done
from keyboards import confirm_menu, func_menu
db = database.DBCommands()


@dp.message_handler(user_id=admin_id, commands=["done"])
async def my_hw(message: types.Message):
    all_done = await db.list_done()
    for num, done in enumerate(all_done):
        text = f'id = {done.id}\nstudent_id = {done.student_id}\n' \
               f'hw_id = {done.homework_id}\nsuccessful = {done.successful}'
        await message.answer(text)


@dp.message_handler(user_id=admin_id, commands=["count_user"])
async def count_user(message: types.Message):
    count_users = await db.count_users()
    text = f'В базе {count_users} пользователей'
    await message.answer(text)


@dp.message_handler(user_id=admin_id, commands=["count_hw"])
async def count_user(message: types.Message):
    count_hw = await db.count_hw()
    text = f'В базе {count_hw} ДЗ'
    await message.answer(text)


@dp.message_handler(user_id=admin_id, commands=["rating"])
async def user_rating(message: types.Message):
    users_marks = db.rating()
    for num, mark in enumerate(users_marks):
        text = f'{mark}'
        await message.answer(text)


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
async def add_description(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.description = description
    await message.answer(f"Пришлите файл ДЗ")
    await NewHW.Document.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Document, content_types=types.ContentType.DOCUMENT)
async def add_document(message: types.Message, state: FSMContext):
    document = message.document.file_id
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.file = document
    await message.answer(f"Пришлите файл ответов")
    await NewHW.Answer.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Answer, content_types=types.ContentType.DOCUMENT)
async def add_document(message: types.Message, state: FSMContext):
    document = message.document.file_id
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.answer = document
    text = f"Название: {hw.title}\nОписание: {hw.description}"
    await message.answer_document(document=hw.file, caption=text)
    await message.answer("Подтверждаете? Нажмите /cancel чтобы отменить", reply_markup=confirm_menu)
    await NewHW.Confirm.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Confirm)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    hw: HW = data.get("hw")
    await hw.create()
    all_user = await db.list_user()
    for num, user in enumerate(all_user):
        new_done = Done()
        new_done.student_id = user.id
        new_done.homework_id = hw.id
        await new_done.create()
    await message.answer('ДЗ успешно добавлено', reply_markup=func_menu)
    await state.reset_state()
