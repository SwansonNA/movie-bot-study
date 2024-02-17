from botinit import bot
from states.state_manager import HighStates, Start
from keyboard.keyboard import BASIC_KEYBOARD
from utilities.supporting_funcs import get_pages_from_api, movies_generator, command_logger
from utilities.keyboard_answer import answer
from telebot.types import Message


@bot.message_handler(state=Start.start, commands=['high'])
def high(msg: Message) -> None:
    """Начало работы команды /high, пользователь вводит число отображаемых фильмов"""

    command_logger(msg, command_name='high')
    bot.send_message(msg.chat.id, "Вы выбрали функцию для отображения лучших фильмов (Рейтинг на IMDB от 8 до 10).\n"
                                  "Введите количество отображаемых фильмов(от 1 до 25).",
                     reply_markup=BASIC_KEYBOARD.hide_keyboard)
    bot.set_state(msg.from_user.id, HighStates.high_start, msg.chat.id)


@bot.message_handler(state=HighStates.high_start, is_digit=True)
def get_pages(msg: Message) -> None:
    """
    Получение страниц из реквеста в кинопоиск
    :param msg: число отображаемых фильмов
    :return:
    """
    global movies_amt
    global pages
    movies_amt, pages = get_pages_from_api(msg, rating='8-10', state=HighStates.get_pages)


@bot.message_handler(state=HighStates.get_pages, is_digit=True)
def list_of_movies(msg: Message) -> None:
    """
    Функция создания строки с фильмами
    :param msg: выбранная страница
    :return:
    """
    movies_generator(
        msg, pages, movies_amt, invert=False, rating='8-10', state=HighStates.result
    )


@bot.message_handler(state=HighStates.result)
def result(msg: Message) -> None:
    """Обрабатывает ответ пользователя после результата"""
    answer(msg, high)



