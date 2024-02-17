from botinit import bot
from telebot.types import Message
from states.state_manager import HighStates, LowStates, CustomStates


@bot.message_handler(
    state=[
        LowStates.low_start, LowStates.get_pages, HighStates.high_start,
        HighStates.get_pages, CustomStates.set_titles_amount, CustomStates.set_titles_amount
    ],
    is_digit=False
)
def wrong_inst(msg: Message) -> None:
    """Если пользователь в функции где просят указать число, пользователь указывает другой тип данных, запускается
    данная функция"""
    bot.send_message(msg.chat.id, 'Вы ввели не целое число, пожалуйста, попробуйте ещё раз.')
