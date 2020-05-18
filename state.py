from aiogram.dispatcher.filters.state import StatesGroup, State


class DoneHW(StatesGroup):
    Choose = State()
    Push = State()
    Confirm = State()


class NewHW(StatesGroup):
    Title = State()
    Description = State()
    Document = State()
    Confirm = State()
