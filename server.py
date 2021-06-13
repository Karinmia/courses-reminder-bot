import os
from time import sleep

from flask import Flask, request
from telebot import types, logger as telebot_logger

from bot_handlers import bot
from config import BOT_TOKEN, HOST

telebot_logger.setLevel(telebot_logger.DEBUG)

server = Flask(__name__)

# if bot.get_webhook_info().url != f"https://{HOST}/{BOT_TOKEN}":
#     bot.remove_webhook()
#     sleep(2)
#     bot.set_webhook(url=f"https://{HOST}/{BOT_TOKEN}", certificate=open('webhook_cert.pem', 'r'))


@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode('utf-8'))])
    return 'OK', 200


# @server.route('/', methods=['GET'])
# def index():
#     return 'Home page', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://course-helper-bot-kpi.herokuapp.com/{BOT_TOKEN}')
    return "!", 200


if __name__ == "__main__":
    if bot.get_webhook_info().url != f"https://{HOST}/{BOT_TOKEN}":
        bot.remove_webhook()
        sleep(2)
        bot.set_webhook(url=f'https://course-helper-bot-kpi.herokuapp.com/{BOT_TOKEN}')

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
