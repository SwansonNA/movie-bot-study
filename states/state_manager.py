from telebot.handler_backends import State, StatesGroup


class Start(StatesGroup):
    """Родительский класс старт, отвечает за состояния команды /start"""
    start = State()


class LowStates(Start):
    """Наследник класса старт, отвечает за состояния команды /low"""
    low_start = State()
    get_pages = State()
    result = State()


class HighStates(Start):
    """Наследник класса старт, отвечает за состояния команды /high"""
    high_start = State()
    get_pages = State()
    result = State()


class CustomStates(Start):
    """Наследник класса старт, отвечает за состояния команды /custom"""
    custom_start = State()
    set_titles_amount = State()
    set_pages = State()
    result = State


class RandomTitle(Start):
    random_start = State()
