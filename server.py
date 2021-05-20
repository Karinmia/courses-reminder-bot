from time import sleep

import flask
from telebot import types, logger as telebot_logger

from bot_handlers import bot
from config import BOT_TOKEN, HOST

telebot_logger.setLevel(telebot_logger.DEBUG)

server = flask.Flask(__name__)

if bot.get_webhook_info().url != f"https://{HOST}/{BOT_TOKEN}":
    bot.remove_webhook()
    sleep(2)
    bot.set_webhook(url=f"https://{HOST}/{BOT_TOKEN}", certificate=open('webhook_cert.pem', 'r'))


@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode('utf-8'))])
    return 'OK', 200


@server.route('/', methods=['GET'])
def index():
    return 'Home page', 200
