import requests
from requests import Response
import json
from typing import Dict
from config import API_KEY


BASE_URL = "https://api.kinopoisk.dev/v1.4/"
headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}


def api_filtered_search(amt: int, rating: (str, int), page=1) -> Response:
    """
    Запрос в API по фильтрам
    :param amt: Кол-во отображаемых фильмов
    :param rating: Рейтинг
    :param page: выбранная страница
    :return: Ответ от API
    """
    response = requests.get(
        f'{BASE_URL}movie?page={page}'
        f'&limit={amt}&selectFields=name&selectFields=shortDescription&selectFields=rating&notNullFields=name&type=movie'
        f'&rating.imdb={rating}',
        headers=headers
    )
    return response


def api_random_title() -> json:
    """Запрос в API, на случайный тайтл"""
    response = requests.get(
        f'{BASE_URL}movie/random?notNullFields=name&notNullFields=description&notNullFields=poster.url&notNullFields=rating.imdb&notNullFields=ageRating&type=movie',
        headers=headers
    ).json()
    return response

