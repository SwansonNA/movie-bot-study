import requests
import json
from typing import Dict
from config import API_KEY


BASE_URL = "https://api.kinopoisk.dev/v1.4/"
headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY
}


def lower_movie(amt: int):
    response = requests.get(
        f'{BASE_URL}movie?page=1&limit={amt}&selectFields=name&selectFields=shortDescription&selectFields=rating&type=movie&rating.imdb=1-4',
        headers=headers
    ).json()
    return response




