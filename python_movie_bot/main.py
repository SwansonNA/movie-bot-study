from botinit import bot
from telebot.types import BotCommand
import handlers


if __name__ == "__main__":
    
    # bot.set_my_commands([BotCommand('hello', 'сказать привет')])
    bot.infinity_polling()
