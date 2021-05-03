import datetime
from time import sleep
from secrets import token_urlsafe

from bot_object import bot
from models import User
from languages import DICTIONARY
from keyboards import *


def login_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            DICTIONARY['ru']['welcome_msg'].format(user.first_name),
            reply_markup=categories_inline_keyboard()
        )
    else:
        return True, 'main_menu_state'
    return False, ''


def main_menu_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY['ru']['mainmenu_msg'],
            reply_markup=get_main_menu_keyboard(language='ru'))
    else:
        if message.text == DICTIONARY['ru']['my_events_btn']:
            bot.send_message(message.chat.id, "Тут будут ивенты, на которые ты подпишешься")
            return True, 'main_menu_state'
        elif message.text == DICTIONARY['ru']['settings_btn']:
            bot.send_message(message.chat.id, "Тут будут твои настройки")
            return True, 'main_menu_state'
        else:
            bot.send_message(message.chat.id, DICTIONARY['ru']['no_button'])

    return False, ''
