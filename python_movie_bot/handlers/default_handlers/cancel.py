from botinit import bot
from telebot.types import Message
from states import state_manager

@bot.message_handler(state='*', commands=['cancel'])
def cancel(msg: Message):
    bot.send_message(msg.chat.id, "Вы вернулись в главное меню")
    bot.delete_state(msg.from_user.id, msg.chat.id)