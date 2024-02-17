from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove


class Keyboard:
    """Базовый класс клавиатуры"""
    def __init__(self):
        self.keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        self.hide_keyboard = ReplyKeyboardRemove()


class BinaryAnswer(Keyboard):
    """Класс клавиатура, выводит да/нет"""
    def __init__(self):
        super().__init__()
        self.keyboard.add('Да', 'Нет', row_width=2)


BASIC_KEYBOARD = Keyboard()
BINARY_KEYBOARD = BinaryAnswer()
