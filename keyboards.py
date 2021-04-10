from telebot import types
from languages import DICTIONARY


def get_main_menu_keyboard(language='ru'):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['my_events_btn'])
    keyboard.add(DICTIONARY[language]['settings_btn'])
    return keyboard
