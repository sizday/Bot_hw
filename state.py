from aiogram.dispatcher.filters.state import StatesGroup, State


class DoneHW(StatesGroup):
    Choose = State()
    Push = State()
    Confirm = State()


class NewHW(StatesGroup):
    Title = State()
    Type = State()
    Description = State()
    Document = State()
    Answer = State()
    Confirm = State()
