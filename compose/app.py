from aiogram import executor
from preload.load_all import bot
from database.database import create_db


async def on_shutdown():
    await bot.close()


async def on_startup():
    await create_db()


if __name__ == '__main__':
    from users.teacher_panel import dp
    from users.student_panel import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
