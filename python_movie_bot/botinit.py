import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from config import BOT_TOKEN

storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
