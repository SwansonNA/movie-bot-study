from botinit import bot
from states.state_manager import Start


@bot.message_handler(state=Start.start)
def repeater(message) -> None:
    """Выводит при вводе неверной команды."""
    bot.reply_to(message, 'К сожалению такой команды, нет воспользуйтесь /help, чтобы узнать доступные команды.')