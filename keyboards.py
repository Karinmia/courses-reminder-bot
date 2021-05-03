from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from enums import CATEGORIES
from languages import DICTIONARY


def get_main_menu_keyboard(language='ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['my_events_btn'])
    keyboard.add(DICTIONARY[language]['settings_btn'])
    return keyboard


def categories_inline_keyboard(language='ru', categories=CATEGORIES):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=DICTIONARY[language]['done_btn'], callback_data="save_categories"))

    # split categories list into smaller lists (with lenght = 3)
    chunks = [CATEGORIES[x:x + 3] for x in range(0, len(CATEGORIES), 3)]
    for chunk in chunks:
        buttons = []
        for btn in chunk:
            buttons.append(InlineKeyboardButton(btn, callback_data=f"{btn}_on"))

        keyboard.add(*buttons)

    return keyboard


def get_skip_keyboard(language='ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['skip_btn'])
    return keyboard
