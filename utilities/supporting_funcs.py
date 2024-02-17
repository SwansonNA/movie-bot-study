from botinit import bot
from telebot.types import Message
from telebot.handler_backends import State
from typing import Dict
from api import api_filtered_search
from database.models import Command
from keyboard.keyboard import BINARY_KEYBOARD
import datetime


def movie_description(response: Dict) -> tuple[str, str]:
    """
    Создает строку с карточкой фильма и возвращает его постер
    :param response: JSON запрос
    :return: tuple[str, str]
    """
    name, rating, year, age_restriction, description, image_url = (
        response['name'], response['rating']['imdb'], response['year'], response['ageRating'], response['description'],
        response['poster']['url']
    )
    genres = ', '.join([genre['name'] for genre in response['genres']])
    movie_portfolio = ('{name} ({year})\n'
                       'Оценка на IMDB: {rating}\n'
                       'Жанр: {genres}\n'
                       'Возраст: {age_restriction}+\n'
                       '{description}').format(
        name=name,
        year=year,
        rating=rating,
        genres=genres,
        age_restriction=age_restriction,
        description=description
    )
    return movie_portfolio, image_url


def movies_from_json(response: Dict, inverted=False) -> str:
    """
    Функция для создания строки с полученными фильмами из JSON
    :param response: ответ от API
    :param inverted: инвертировать список по рейтингу, по-умолчанию не инвертирует
    :return:
    """
    movies = list()

    for i_movie in response['docs']:
        entry = dict()
        entry['Название'] = i_movie['name']
        entry['Рейтинг'] = i_movie['rating']['imdb']
        # Иногда в кинопоиске нет короткого описания того или иного фильма
        if i_movie['shortDescription'] is None:
            entry['Описание'] = 'К сожалению у этого фильма нет описания'
        else:
            entry['Описание'] = i_movie['shortDescription']
        movies.append(entry)

    if inverted:
        movies = sorted(movies, key=lambda rating: rating['Рейтинг'])
    else:
        movies = sorted(movies, key=lambda rating: rating['Рейтинг'], reverse=True)

    text = ''
    counter = 1
    for x in movies:
        text += f"{counter}) {x['Название']} ({x['Рейтинг']}): {x['Описание']}.\n\n"
        counter += 1
    return text


def response_handler(response: Dict) -> str:
    """
    Превращает из технического ответа от апи об ошибке в понятный для пользователя.
    :param response: JSON ответ от API
    :return: str
    """
    if 'Поле rating.imdb должно быть числом или массивом чисел!' in response['message']:
        return 'Рейтинг должен быть числом или массивом чисел, попробуйте снова.'
    elif 'Значение поля rating.imdb должно быть в диапазоне от 0 до 10!' in response['message']:
        return 'Рейтинг должен быть быть в диапазоне от 0 до 10, попробуйте снова.'


def pages_from_response(response: Dict) -> int:
    """Функция возвращающая общее кол-во страниц"""
    total_pages = response['pages']
    return total_pages


def get_pages_from_api(msg: Message, rating: str, state: State) -> tuple[int, int] | None:
    """
    Получает количество страниц исходя из требований пользователя
    :param msg: Кол-во фильмов
    :param rating: Заданный рейтинг
    :param state: Какой state нужно задать по окончанию функции
    :return: Кол-во фильмов на странице, кол-во страниц
    """
    movies_amt = int(msg.text)
    if movies_amt not in range(1, 26):
        bot.send_message(msg.chat.id, f'Количество отображаемых фильмов должно быть от 1 до 25.')
    else:
        bot.send_chat_action(msg.chat.id, 'typing')
        pages = pages_from_response(api_filtered_search(movies_amt, rating, page=1).json())
        bot.send_message(msg.chat.id, f'Выберите страницу от 1 до {pages}.')
        bot.set_state(msg.from_user.id, state, msg.chat.id)
        return movies_amt, pages


def movies_generator(msg: Message, pages: int, movies_amt: int, invert: bool, rating: str, state: State) -> None:
    """
    Переводит ответ от API в строку с фильмами по рейтингу
    :param msg: Выбранная страница
    :param pages: Кол-во страниц
    :param movies_amt: Кол-во отображаемых фильмов
    :param invert: Инвертировать рейтинг или нет
    :param rating: Заданный рейтинг
    :param state: Какой state нужно задать по окончанию функции
    :return:
    """
    page = int(msg.text)
    if pages not in range(1, pages + 1):
        bot.send_message(msg.chat.id, f'Число должно быть от 1 до {pages}.')
    else:
        bot.send_chat_action(msg.chat.id, 'typing')
        movies = movies_from_json(api_filtered_search(movies_amt, rating, page=int(msg.text)).json(), inverted=invert)
        bot.send_message(msg.chat.id, movies)
        bot.set_state(msg.from_user.id, state, msg.chat.id)
        bot.send_message(msg.chat.id, 'Хотите повторить поиск?', reply_markup=BINARY_KEYBOARD.keyboard)


def command_logger(msg: Message, command_name: str):
    """
    Логгирует введенные команды пользователем
    :param msg: Введенная команда
    :param command_name: Название команды
    :return:
    """
    user_id = msg.from_user.id
    unix_date = msg.date
    date = datetime.datetime.fromtimestamp(unix_date)
    command = Command(
        user_id=user_id,
        command_name=command_name,
        when_requested=date
    )
    command.save()
