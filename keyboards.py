from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from enums import CATEGORIES
from languages import DICTIONARY
from database import session
from models import UserSubscription


def get_main_menu_keyboard(language='ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['my_events_btn'])
    keyboard.add(DICTIONARY[language]['settings_btn'])
    return keyboard


def get_settings_menu_keyboard(language='ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        DICTIONARY[language]['settings_categories_btn'],
        DICTIONARY[language]['settings_city_btn']
    )
    keyboard.add(DICTIONARY[language]['back_button'])
    return keyboard


def categories_inline_keyboard(language='ru', categories=CATEGORIES, user=None):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=DICTIONARY[language]['done_btn'], callback_data="save_categories"))

    # split categories list into smaller lists (with lenght = 3)
    chunks = [CATEGORIES[x:x + 3] for x in range(0, len(CATEGORIES), 3)]

    subscriptions_name = [s.name for s in user.subscriptions.all()]

    for chunk in chunks:
        buttons = []
        for btn in chunk:
            if btn in subscriptions_name:
                buttons.append(InlineKeyboardButton(f"{btn} ✅ ", callback_data=f"{btn}_on"))
            else:
                buttons.append(InlineKeyboardButton(btn, callback_data=f"{btn}_on"))

        keyboard.add(*buttons)

    return keyboard


def get_skip_keyboard(language='ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['skip_btn'])
    return keyboard
