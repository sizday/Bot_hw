from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="confirm"),
            KeyboardButton(text="/cancel"),
        ],
    ],
    resize_keyboard=True
)

func_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/add_hw"),
            KeyboardButton(text="/hw"),
        ],
    ],
    resize_keyboard=True
)

type_hw_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Test'),
            KeyboardButton(text='Grammar'),
        ],
        [
            KeyboardButton(text='Python'),
            KeyboardButton(text='Picture'),
        ]
    ],
    resize_keyboard=True
)
