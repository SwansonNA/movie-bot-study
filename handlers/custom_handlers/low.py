from botinit import bot
from telebot.types import Message
from states.state_manager import LowStates, Start
from keyboard.keyboard import BASIC_KEYBOARD
from utilities.supporting_funcs import get_pages_from_api, movies_generator, command_logger
from utilities.keyboard_answer import answer


@bot.message_handler(state=Start.start, commands=['low'])
def low(msg: Message) -> None:
    """Начало работы команды /low, пользователь вводит число отображаемых фильмов"""

    command_logger(msg, command_name='low')
    bot.send_message(msg.chat.id, "Вы выбрали функцию для отображения худших фильмов (Рейтинг на IMDB от 1 до 4).\n"
                                  "Введите количество отображаемых фильмов(от 1 до 25).",
                     reply_markup=BASIC_KEYBOARD.hide_keyboard)
    bot.set_state(msg.from_user.id, LowStates.low_start, msg.chat.id)


@bot.message_handler(state=LowStates.low_start, is_digit=True)
def get_pages(msg: Message) -> None:
    """
    Проверяет, находится ли ответ пользователя в диапазоне, запрашивает отображаемую страницу.
    :param msg: Кол-во отображаемых фильмов
    :return:
    """
    global movies_amt
    global pages
    movies_amt, pages = get_pages_from_api(msg, rating='1-4', state=LowStates.get_pages)


@bot.message_handler(state=LowStates.get_pages, is_digit=True)
def list_of_movies(msg: Message) -> None:
    """
    Генерирует строку фильмов.
    :param msg: Страница
    :return:
    """
    movies_generator(
        msg, pages, movies_amt, invert=True, rating='1-4', state=LowStates.result
    )


@bot.message_handler(state=LowStates.result)
def result(msg: Message) -> None:
    """Обрабатывает ответ пользователя после результата."""
    answer(msg, low)




