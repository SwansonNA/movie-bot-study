from api import api_filtered_search
from botinit import bot
from states.state_manager import CustomStates, Start
from keyboard.keyboard import BASIC_KEYBOARD
from utilities.supporting_funcs import response_handler, get_pages_from_api, movies_generator, command_logger
from utilities.keyboard_answer import answer
from telebot.types import Message


@bot.message_handler(state=Start.start, commands=['custom'])
def custom(msg: Message) -> None:
    """Начало работы команды /custom, запрашивает нужный рейтинг у пользователя"""

    command_logger(msg, command_name='custom')
    bot.send_message(msg.chat.id, "Вы выбрали функцию для отображения фильмов c пользовательскими настройками.\n"
                                  "Вы можете выбрать отображение фильмов по вашему фильтру оценок.\n"
                                  "Оценки должны быть от 1 до 10 (пример: 7, 10, 7-10).",
                     reply_markup=BASIC_KEYBOARD.hide_keyboard)
    bot.set_state(msg.from_user.id, CustomStates.custom_start, msg.chat.id)


@bot.message_handler(state=CustomStates.custom_start)
def titles_amount(msg: Message) -> None:
    """
    Проверяет ввел ли пользователь рейтинг верно, запрашивает кол-во отображаемых фильмов
    :param msg: Оценка
    :return:
    """
    global rating
    rating = msg.text
    response = api_filtered_search(amt=1, rating=rating, page=1)
    response_text = response.json()
    if response.status_code == 400:
        response = response_handler(response_text)
        bot.send_message(msg.chat.id, response)
    else:
        bot.send_message(msg.chat.id, 'Введите количество отображаемых фильмов (от 1 до 25).')
        bot.set_state(msg.from_user.id, CustomStates.set_titles_amount, msg.chat.id)


@bot.message_handler(state=CustomStates.set_titles_amount, is_digit=True)
def set_pages(msg: Message) -> None:
    """
    Проверяет, находится ли ответ пользователя в диапазоне, запрашивает отображаемую страницу.
    :param msg: Кол-во отображаемых фильмов
    :return:
    """
    global pages
    global movies_amt
    movies_amt, pages = get_pages_from_api(msg, rating, state=CustomStates.set_pages)


@bot.message_handler(state=CustomStates.set_pages, is_digit=True)
def list_of_movies(msg: Message) -> None:
    """
    Генерирует строку фильмов.
    :param msg: Страница
    :return:
    """
    movies_generator(
        msg, pages, movies_amt, invert=False, rating=rating, state=CustomStates.result
    )


@bot.message_handler(state=CustomStates.result)
def result(msg: Message) -> None:
    """Обрабатывает ответ пользователя после результата."""
    answer(msg, custom)
