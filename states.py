import datetime
from time import sleep

from bot_object import bot
from database import session
from models import User, SupportRequest, SupportResponse
from keyboards import *
from languages import DICTIONARY
from parser import delete_events
from utils import (
    get_events_from_db_for_user, get_events_for_user, format_events_as_message, get_support_requests
)


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
            reply_markup=get_main_menu_keyboard(role=user.role, language=user.language))
    else:
        if message.text == DICTIONARY[user.language]['my_events_btn']:
            if user_events := get_events_for_user(user):
                for event in user_events:
                    events_msg = format_events_as_message(event)
                    bot.send_message(
                        message.chat.id, text=events_msg, parse_mode='Markdown',
                        reply_markup=get_unsubscribe_keyboard(obj_id=event.id, language=user.language)
                    )
            else:
                events_msg = DICTIONARY[user.language]['no_events_msg']
                bot.send_message(message.chat.id, text=events_msg)
            return False, 'main_menu_state'

        elif message.text == DICTIONARY[user.language]['get_events_btn']:
            # send message with list of events
            if events := get_events_from_db_for_user(user):
                events_ids = [obj.id for obj in events]
                events_msg = format_events_as_message(events)
                bot.send_message(
                    message.chat.id, text=events_msg, parse_mode='Markdown',
                    reply_markup=events_inline_keyboard(events_ids, user, language=user.language)
                )
            else:
                events_msg = DICTIONARY[user.language]['no_events_msg']
                bot.send_message(message.chat.id, text=events_msg)
            return False, 'main_menu_state'

        elif message.text == DICTIONARY[user.language]['settings_btn']:
            return True, 'settings_menu_state'
        elif message.text == DICTIONARY[user.language]['support_btn']:
            return True, 'support_menu_state'
        elif message.text == DICTIONARY[user.language]['admin_menu_btn']:
            return True, 'admin_menu_state'
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
            bot.send_message(
                message.chat.id,
                DICTIONARY[user.language]['set_categories_msg'],
                reply_markup=categories_inline_keyboard(user=user, language=user.language)
            )
            return False, 'settings_menu_state'
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


def support_menu_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['support_menu_msg'],
            reply_markup=get_back_keyboard(language=user.language))
    else:
        if message.text == DICTIONARY[user.language]['back_btn']:
            return True, 'main_menu_state'
        else:
            support_request = SupportRequest(user_id=user.id, message=message.text[:300])
            session.add(support_request)
            session.commit()
            bot.send_message(message.chat.id, DICTIONARY[user.language]['sent_support_request_msg'])
            return True, 'main_menu_state'

    return False, ''


def admin_menu_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['admin_menu_msg'],
            reply_markup=get_admin_menu_keyboard(language=user.language))
    else:
        if message.text == DICTIONARY[user.language]['support_btn']:
            bot.send_message(message.chat.id, DICTIONARY[user.language]['admin_support_menu_msg'])
            # send list of support requests with inline button "Respond" per each
            s_requests = get_support_requests()
            for obj in s_requests:
                bot.send_message(
                    message.chat.id, text=obj.message,
                    reply_markup=get_admin_support_request_keyboard(obj_id=obj.id, language=user.language))
            return False, 'admin_menu_state'
        elif message.text == DICTIONARY[user.language]['clear_events_btn']:
            deleted_events = delete_events()
            bot.send_message(
                message.chat.id,
                DICTIONARY[user.language]['clear_events_success_msg'].format(deleted_events)
            )
            return False, 'admin_menu_state'
        if message.text == DICTIONARY[user.language]['mainmenu_msg']:
            return True, 'main_menu_state'
        else:
            bot.send_message(message.chat.id, DICTIONARY[user.language]['no_button'])

    return False, ''


def admin_support_respond_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id, DICTIONARY[user.language]['admin_respond_msg'],
            reply_markup=get_back_keyboard(language=user.language))
    else:
        if message.text == DICTIONARY[user.language]['back_btn']:
            return True, 'admin_menu_state'
        else:
            # create SupportRespond
            pass

    return False, ''
