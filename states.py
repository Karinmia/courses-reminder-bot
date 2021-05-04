import datetime
from time import sleep

from bot_object import bot
from database import session
from models import User
from keyboards import *
from languages import DICTIONARY


def login_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            DICTIONARY['ru']['welcome_msg'].format(user.first_name),
            reply_markup=categories_inline_keyboard(user=user)
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
            # bot.send_message(message.chat.id, "Тут будут твои настройки")
            return True, 'settings_menu_state'
        else:
            bot.send_message(message.chat.id, DICTIONARY['ru']['no_button'])

    return False, ''


def set_city_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY['ru']['set_city_msg'],
            reply_markup=get_skip_keyboard(language='ru'))
    else:
        if message.text == DICTIONARY['ru']['skip_btn']:
            bot.send_message(message.chat.id, DICTIONARY['ru']['signed_up_msg'])
            return True, 'main_menu_state'
        else:
            # TODO: check if given city exists in Ukraine
            user.city = message.text
            session.commit()
            bot.send_message(message.chat.id, DICTIONARY['ru']['signed_up_msg'])
            return True, 'main_menu_state'

    return False, ''


def settings_menu_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY['ru']['settings_menu_msg'],
            reply_markup=get_settings_menu_keyboard(language='ru'))
    else:
        if message.text == DICTIONARY['ru']['settings_categories_btn']:
            bot.send_message(message.chat.id, "В разработке...")
            return True, 'settings_menu_state'
        elif message.text == DICTIONARY['ru']['settings_city_btn']:
            return True, 'change_city_state'
        elif message.text == DICTIONARY['ru']['back_btn']:
            return True, 'main_menu_state'
        else:
            bot.send_message(message.chat.id, DICTIONARY['ru']['no_button'])

    return False, ''


def change_city_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, "Введи название города:",
            reply_markup=get_back_keyboard(language='ru')
        )
    else:
        if message.text == DICTIONARY['ru']['back_btn']:
            return True, 'settings_menu_state'
        else:
            # TODO: check if given city exists in Ukraine
            user.city = message.text
            session.commit()
            bot.send_message(message.chat.id, "Город успешно обновлен")
            return True, 'main_menu_state'

    return False, ''
