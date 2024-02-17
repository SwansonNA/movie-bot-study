from api import api_random_title
from botinit import bot
from states.state_manager import Start, RandomTitle
from keyboard.keyboard import BASIC_KEYBOARD, BINARY_KEYBOARD
from utilities.supporting_funcs import command_logger, movie_description
from utilities.keyboard_answer import answer
from telebot.types import Message


@bot.message_handler(commands=['random'], state=Start.start)
def start_random(msg: Message) -> None:
    """Выводит случайный тайтл из кинопоиска"""
    command_logger(msg, command_name='random')
    bot.send_message(msg.chat.id, 'Ищу случайный фильм...', reply_markup=BASIC_KEYBOARD.hide_keyboard)
    bot.send_chat_action(msg.chat.id, 'typing')
    movie_portfolio, poster_url = movie_description(api_random_title())
    bot.send_photo(msg.chat.id, photo=poster_url)
    bot.send_message(msg.chat.id, movie_portfolio)
    bot.send_message(msg.chat.id, 'Хотите попытать удачу ещё раз?', reply_markup=BINARY_KEYBOARD.keyboard)
    bot.set_state(msg.from_user.id, RandomTitle.random_start, msg.chat.id)


@bot.message_handler(state=RandomTitle.random_start)
def result(msg: Message) -> None:
    answer(msg, func=start_random)


