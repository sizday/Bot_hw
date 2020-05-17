from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rps_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Rock"),
            KeyboardButton(text="Paper"),
            KeyboardButton(text="Scissors")
        ],
    ],
    resize_keyboard=True
)