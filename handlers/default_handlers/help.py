from botinit import bot
from telebot.types import Message
from utilities.all_commands import commands


@bot.message_handler(commands=['help'])
def show_commands(message: Message) -> None:
    """Выводит доступные команды в боте"""
    str_commands = '\n'.join(f'/{i_command} {j_description}' for i_command, j_description in commands)
    bot.send_message(message.chat.id, str_commands)
