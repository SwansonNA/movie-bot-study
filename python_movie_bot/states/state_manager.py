from telebot.handler_backends import State, StatesGroup


class StatesManager(StatesGroup):
    start = State()
    lower = State()
    lower_api = State()
    cancel = State()
