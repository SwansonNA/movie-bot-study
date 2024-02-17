from botinit import bot
from telebot.types import Message


@bot.message_handler(commands=['hello'])
def send_hello(message: Message):
    bot.send_message(message.chat.id, 'Hello, World!')