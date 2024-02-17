from botinit import bot
from telebot.types import Message
from typing import Callable
from states.state_manager import Start
from keyboard.keyboard import BINARY_KEYBOARD


# @bot.message_handler(state=[StatesHighManager.result ,StatesLowManager.result, StatesCustomManager.result])
def answer(msg: Message, func: Callable) -> None:
    """
    Функция, которая выводит пользователя из команды в главное меню или запускаем её заново
    :param msg: Ответ из markup
    :param func: Начальная функция команды
    :return:
    """
    reply = msg.text
    # Чтобы не париться со стейтами и выводами сообщений сразу запускаем функцию начала, там всё само установится и
    # напишется
    if reply == 'Да':
        func(msg)
    elif reply == 'Нет':
        bot.send_message(msg.chat.id, 'Возвращаю в главное меню.', reply_markup=BINARY_KEYBOARD.hide_keyboard) # TODO Поменять на все доступные команды.
        bot.set_state(msg.from_user.id, Start.start, msg.chat.id)
    else:
        bot.send_message(msg.chat.id, 'Воспользуйтесь пожалуйста клавиатурой снизу.')