from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from config import CATEGORIES
from languages import DICTIONARY


def get_main_menu_keyboard(language='ru'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['my_events_btn'])
    keyboard.add(DICTIONARY[language]['settings_btn'])
    return keyboard


def categories_keyboard(language='ru', categories=[]):
    """Just an example keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('python', 'js', 'PHP')
    keyboard.add('C#', 'Java', 'QA')
    keyboard.add('Data Science', 'Embedded')
    return keyboard


def categories_inline_keyboard(language='ru', categories=CATEGORIES):
    keyboard = InlineKeyboardMarkup()

    # split categories list into smaller lists (with lenght = 3)
    chunks = [CATEGORIES[x:x + 3] for x in range(0, len(CATEGORIES), 3)]
    for chunk in chunks:
        buttons = []
        for btn in chunk:
            buttons.append(InlineKeyboardButton(btn, callback_data=btn))
        keyboard.add(*buttons)

    return keyboard
