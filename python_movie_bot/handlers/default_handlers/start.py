from botinit import bot
from telebot.types import Message
from states import state_manager


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.set_state(message.from_user.id, state_manager.StatesManager.start)
    bot.send_message(message.chat.id, f'Добро пожаловать в кинобот, {message.from_user.full_name}!\n'
                                      f'Чтобы узнать функционал введите /help')
    print(bot.current_states.get_state(message.chat.id, message.from_user.id))
