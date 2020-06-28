from aiogram import executor
from load_all import bot
from database import create_db


async def on_shutdown():
    await bot.close()


async def on_startup():
    await create_db()


if __name__ == '__main__':
    from teacher_panel import dp
    from student_panel import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
