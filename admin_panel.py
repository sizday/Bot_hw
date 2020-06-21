from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from state import NewHW
import database
from config import admin_id
from load_all import dp
from database import HW, User, Done
from keyboards import confirm_menu, func_menu, type_hw_menu, lang_menu
db = database.DBCommands()

'''
@dp.message_handler(user_id=admin_id, Command("done"))
async def my_hw(message: Message):
    all_done = await db.list_done()
    for num, done in enumerate(all_done):
        text = f'id = {done.id}\nstudent_id = {done.student_id}\n' \
               f'hw_id = {done.homework_id}\nsuccessful = {done.successful}'
        await message.answer(text)
'''


@dp.message_handler(Command("count_user"), user_id=admin_id)
async def count_user(message: Message):
    count_users = await db.count_users()
    text = f'В базе {count_users} пользователей'
    await message.answer(text)


@dp.message_handler(Command("cancel"), user_id=admin_id, state=NewHW)
async def cancel(message: Message, state: FSMContext):
    await message.answer("Вы отменили добавление ДЗ")
    await state.reset_state()


@dp.message_handler(Command("add_hw"), user_id=admin_id)
async def add_item(message: Message):
    await message.answer("Введите название ДЗ или нажмите /cancel")
    await NewHW.Title.set()


@dp.message_handler(user_id=admin_id, state=NewHW.Title)
async def enter_name(message: Message, state: FSMContext):
    name = message.text
    hw = HW()
    hw.title = name
    await message.answer(f"Название: {name}\nПришлите мне описание или нажмите /cancel")
    await NewHW.Description.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Description)
async def add_description(message: Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.description = description
    await message.answer(f"Пришлите тип ДЗ или /cancel", reply_markup=type_hw_menu)
    await NewHW.Type.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Type)
async def add_type(message: Message, state: FSMContext):
    type_hw = message.text
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.type = type_hw
    await message.answer(f"Пришлите файл ДЗ или нажмите /cancel")
    await NewHW.Document.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Document, content_types=types.ContentType.DOCUMENT)
async def add_document(message: Message, state: FSMContext):
    document = message.document.file_id
    data = await state.get_data()
    hw: HW = data.get("hw")
    hw.file = document
    await state.update_data(hw=hw)
    if hw.type != 'Grammar':
        await message.answer(f"Пришлите файл ответов или /cancel")
        await NewHW.Answer.set()
    else:
        text = f"Название: {hw.title}\nОписание: {hw.description}"
        await message.answer_document(document=hw.file, caption=text)
        await message.answer("Подтверждаете? Нажмите /cancel чтобы отменить", reply_markup=confirm_menu)
        await NewHW.Confirm.set()


@dp.message_handler(user_id=admin_id, state=NewHW.Answer, content_types=types.ContentType.DOCUMENT)
async def add_answer_document(message: Message, state: FSMContext):
    data = await state.get_data()
    hw: HW = data.get("hw")
    document = message.document.file_id
    hw.answer = document
    text = f"Название: {hw.title}\nОписание: {hw.description}"
    await message.answer_document(document=hw.file, caption=text)
    await message.answer("Подтверждаете? Нажмите /cancel чтобы отменить", reply_markup=confirm_menu)
    await NewHW.Confirm.set()
    await state.update_data(hw=hw)


@dp.message_handler(user_id=admin_id, state=NewHW.Confirm)
async def enter_price(message: Message, state: FSMContext):
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


@dp.message_handler(Command('rating'))
async def rating(message: Message):
    users_marks_dict = await db.list_all_marks()
    text = 'Студент Средний балл\n'
    for key, value in users_marks_dict.items():
        text += f'{key} - {value}\n'
    await message.answer(text)
