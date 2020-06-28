from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from state import NewHW
from load_all import dp
from database import HW, Done, DBCommands
from keyboards import confirm_menu, func_menu, type_hw_menu

db = DBCommands()


@dp.message_handler(Command("count_user"))
async def count_user(message: Message):
    if db.is_teacher():
        count_users = await db.count_users()
        text = f'В базе {count_users} пользователей'
        await message.answer(text)


@dp.message_handler(Command("cancel"), state=NewHW)
async def cancel(message: Message, state: FSMContext):
    if db.is_teacher():
        await message.answer("Вы отменили добавление ДЗ")
        await state.reset_state()


@dp.message_handler(Command("add_hw"))
async def add_item(message: Message):
    if db.is_teacher():
        await message.answer("Введите название ДЗ или нажмите /cancel")
        await NewHW.Title.set()


@dp.message_handler(state=NewHW.Title)
async def enter_name(message: Message, state: FSMContext):
    if db.is_teacher():
        name = message.text
        hw = HW()
        hw.title = name
        await message.answer(f"Название: {name}\nПришлите мне описание или нажмите /cancel")
        await NewHW.Description.set()
        await state.update_data(hw=hw)


@dp.message_handler(state=NewHW.Description)
async def add_description(message: Message, state: FSMContext):
    if db.is_teacher():
        description = message.text
        data = await state.get_data()
        hw: HW = data.get("hw")
        hw.description = description
        await message.answer(f"Пришлите тип ДЗ или /cancel", reply_markup=type_hw_menu)
        await NewHW.Type.set()
        await state.update_data(hw=hw)


@dp.message_handler(state=NewHW.Type)
async def add_type(message: Message, state: FSMContext):
    if db.is_teacher():
        type_hw = message.text
        data = await state.get_data()
        hw: HW = data.get("hw")
        hw.type = type_hw
        await message.answer(f"Пришлите файл ДЗ или нажмите /cancel")
        await NewHW.Document.set()
        await state.update_data(hw=hw)


@dp.message_handler(state=NewHW.Document, content_types=types.ContentType.DOCUMENT)
async def add_document(message: Message, state: FSMContext):
    if db.is_teacher():
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


@dp.message_handler(state=NewHW.Answer, content_types=types.ContentType.DOCUMENT)
async def add_answer_document(message: Message, state: FSMContext):
    if db.is_teacher():
        data = await state.get_data()
        hw: HW = data.get("hw")
        document = message.document.file_id
        hw.answer = document
        text = f"Название: {hw.title}\nОписание: {hw.description}"
        await message.answer_document(document=hw.file, caption=text)
        await message.answer("Подтверждаете? Нажмите /cancel чтобы отменить", reply_markup=confirm_menu)
        await NewHW.Confirm.set()
        await state.update_data(hw=hw)


@dp.message_handler(state=NewHW.Confirm)
async def enter_price(message: Message, state: FSMContext):
    if db.is_teacher():
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
    if db.is_teacher():
        users_marks_dict = await db.list_all_marks()
        if not users_marks_dict:
            await message.answer('В рейтинге ни одного ученика')
        else:
            text = 'Студент Средний балл\n'
            for key, value in users_marks_dict.items():
                user = await db.get_user(key)
                text += f'{user.full_name} - {value[0]}\n'
            await message.answer(text)
