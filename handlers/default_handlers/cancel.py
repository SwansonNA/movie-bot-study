from botinit import bot
from telebot.types import Message
from states.state_manager import Start


@bot.message_handler(state='*', commands=['cancel'])
def cancel(msg: Message):
    """Отменяет любую команду, возвращает в главное меню"""
    bot.send_message(msg.chat.id, "Вы вернулись в главное меню")
    bot.set_state(msg.from_user.id, Start.start, msg.chat.id)
