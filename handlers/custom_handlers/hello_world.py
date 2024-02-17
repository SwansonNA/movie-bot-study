from botinit import bot
from telebot.types import Message


@bot.message_handler(commands=['hello'])
def send_hello(message: Message) -> None:
    """Маленькая, секретная команда для тестирования"""
    bot.send_message(message.chat.id, 'Hello, World!')