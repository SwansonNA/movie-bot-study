from botinit import bot
from telebot.types import Message


@bot.message_handler(commands=['help'])
def show_commands(message: Message):
    bot.send_message(message.chat.id, '/start - запуск бота.\n'
                                      '/help - показать доступные команды.\n'
                                      '/hello - поприветствовать мир!')