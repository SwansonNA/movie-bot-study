from botinit import bot


@bot.message_handler(func=lambda message: True)
def repeater(message):
    bot.reply_to(message, message.text)