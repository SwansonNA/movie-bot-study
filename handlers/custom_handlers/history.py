from botinit import bot
from telebot.types import Message
from states.state_manager import Start
from database.models import User, Command
from typing import List
from utilities.supporting_funcs import command_logger


@bot.message_handler(commands=['history'], state=Start.start)
def history(msg: Message) -> None:
    """Выводит историю последних 10 запросов пользователя"""
    user_id = msg.from_user.id
    user = User.get_or_none(User.user_id == user_id)

    commands: List[Command] = user.commands.order_by(-Command.command_id).limit(10)
    commands_history = list()
    commands_history.extend(map(str, reversed(commands)))
    if len(commands_history) == 0:
        bot.send_message(msg.chat.id, 'Вы ещё не использовали команды.')
        return
    bot.send_message(msg.chat.id, 'Вывожу историю последних 10 использованных команд.')
    bot.send_message(msg.chat.id, '\n'.join(commands_history))
    command_logger(msg, command_name='history')