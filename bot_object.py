from config import BOT_TOKEN
import telebot

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
print(bot.get_me())
