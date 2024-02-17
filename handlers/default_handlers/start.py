from botinit import bot
from telebot.types import Message
from states.state_manager import Start
from database.models import User
from peewee import IntegrityError


@bot.message_handler(commands=['start'])
def start(msg: Message) -> None:
    """Запуск бота"""
    user_id = msg.from_user.id
    username = msg.from_user.username
    bot.send_message(msg.chat.id, f'Добро пожаловать в кинобот, {msg.from_user.full_name}!\n'
                                  f'Чтобы узнать функционал введите /help')
    try:
        User.create(
            user_id=user_id,
            username=username
        )
    except IntegrityError:
        pass

    bot.set_state(msg.from_user.id, Start.start, msg.chat.id)
