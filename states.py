import datetime
from time import sleep

from bot_object import bot
from database import session
from models import User
from keyboards import *
from languages import DICTIONARY
from utils import get_events_from_db_for_user, get_events_for_user, format_events_as_message


def set_language_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            DICTIONARY[user.language]['set_lang_msg'].format(user.first_name),
            reply_markup=get_languages_keyboard()
        )
    else:
        if message.text == DICTIONARY['ua_lang_btn']:
            user.language = 'ua'
            session.commit()
            return True, 'login_state'
        elif message.text == DICTIONARY['ru_lang_btn']:
            user.language = 'ru'
            session.commit()
            return True, 'login_state'
        else:
            return True, 'set_language_state'

    return False, ''


def login_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            DICTIONARY[user.language]['welcome_msg'].format(user.first_name),
            reply_markup=categories_inline_keyboard(user=user, language=user.language)
        )
    else:
        return True, 'main_menu_state'
    return False, 'main_menu_state'


def main_menu_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['mainmenu_msg'],
            reply_markup=get_main_menu_keyboard(language=user.language))
    else:
        if message.text == DICTIONARY[user.language]['my_events_btn']:
            user_events = get_events_for_user(user)
            events_message = format_events_as_message(user_events)
            bot.send_message(
                message.chat.id, text=events_message, parse_mode='Markdown'
            )
            return False, 'main_menu_state'
        elif message.text == DICTIONARY[user.language]['settings_btn']:
            return True, 'settings_menu_state'
        elif message.text == DICTIONARY[user.language]['get_events_btn']:
            # send message with list of events
            events = get_events_from_db_for_user(user)
            events_ids = [obj.id for obj in events]
            events_message = format_events_as_message(events)
            bot.send_message(
                message.chat.id, text=events_message, parse_mode='Markdown',
                reply_markup=events_inline_keyboard(events_ids, user, language=user.language)
            )
            return False, 'main_menu_state'
        else:
            bot.send_message(message.chat.id, DICTIONARY[user.language]['no_button'])

    return False, ''


def set_city_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['set_city_msg'],
            reply_markup=get_skip_keyboard(language=user.language))
    else:
        if message.text == DICTIONARY[user.language]['skip_btn']:
            bot.send_message(message.chat.id, DICTIONARY[user.language]['signed_up_msg'])
            return True, 'main_menu_state'
        else:
            # TODO: check if given city exists in Ukraine
            user.city = message.text
            session.commit()
            bot.send_message(message.chat.id, DICTIONARY[user.language]['signed_up_msg'])
            return True, 'main_menu_state'

    return False, ''


def settings_menu_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['settings_menu_msg'],
            reply_markup=get_settings_menu_keyboard(language=user.language))
    else:
        user_lang = user.language
        if message.text == DICTIONARY[user_lang]['settings_categories_btn']:
            bot.send_message(message.chat.id, "В разработке...")
            return True, 'settings_menu_state'
        elif message.text == DICTIONARY[user_lang]['settings_city_btn']:
            return True, 'change_city_state'
        elif message.text == DICTIONARY[user_lang]['back_btn']:
            return True, 'main_menu_state'
        else:
            bot.send_message(message.chat.id, DICTIONARY[user_lang]['no_button'])

    return False, ''


def change_city_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['enter_city_msg'],
            reply_markup=get_back_keyboard(language=user.language)
        )
    else:
        if message.text == DICTIONARY[user.language]['back_btn']:
            return True, 'settings_menu_state'
        else:
            # TODO: check if given city exists in Ukraine
            user.city = message.text
            session.commit()
            bot.send_message(message.chat.id, DICTIONARY[user.language]['saved_city_msg'])
            return True, 'main_menu_state'

    return False, ''
