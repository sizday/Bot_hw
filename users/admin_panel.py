from database.database import DBCommands
from preload.load_all import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from users.admin import Admin

db = DBCommands()
denis = Admin()


@dp.message_handler(Command('add_teacher'))
async def add_teacher(message: Message):
    teacher_id = int(message.text)
    await denis.add_teacher(teacher_id=teacher_id)
    await message.answer(f'Преподователь ')


@dp.message_handler(Command('delete_teacher'))
async def delete_teacher(message: Message):
    teacher_id = int(message.text)
    await denis.delete_teacher(teacher_id=teacher_id)
    await message.answer(f'Преподователь ')
