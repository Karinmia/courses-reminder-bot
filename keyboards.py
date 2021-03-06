from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from enums import CATEGORIES, Roles
from languages import DICTIONARY


def get_languages_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY['ua_lang_btn'], DICTIONARY['ru_lang_btn'])
    return keyboard


def get_main_menu_keyboard(role=Roles.user, language='ua'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        DICTIONARY[language]['get_events_btn'],
        DICTIONARY[language]['my_events_btn']
    )
    keyboard.add(DICTIONARY[language]['settings_btn'], DICTIONARY[language]['support_btn'])

    if role == Roles.admin:
        keyboard.add(DICTIONARY[language]['admin_menu_btn'])

    return keyboard


def get_settings_menu_keyboard(language='ua'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        DICTIONARY[language]['settings_categories_btn'],
        DICTIONARY[language]['settings_city_btn'],
    )
    keyboard.add(DICTIONARY[language]['remove_city_btn'])
    keyboard.add(DICTIONARY[language]['back_btn'])
    return keyboard


def categories_inline_keyboard(categories=CATEGORIES, user=None, language='ua'):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=DICTIONARY[language]['done_btn'], callback_data="save_categories"))

    # split categories list into smaller lists (with length = 3)
    chunks = [categories[x:x + 3] for x in range(0, len(categories), 3)]

    subscriptions_name = [s.name for s in user.subscriptions.all()]

    for chunk in chunks:
        buttons = []
        for btn in chunk:
            if btn in subscriptions_name:
                buttons.append(InlineKeyboardButton(f"{btn} ✅ ", callback_data=f"category_{btn}"))
            else:
                buttons.append(InlineKeyboardButton(btn, callback_data=f"category_{btn}"))
        keyboard.add(*buttons)

    return keyboard


def events_inline_keyboard(events_ids=[], user=None, language='ua'):
    keyboard = InlineKeyboardMarkup(row_width=7)

    user_events_ids = [obj.event_id for obj in user.events.all()]
    buttons = [InlineKeyboardButton("<", callback_data=f"page_down")]

    for i, event_id in enumerate(events_ids):  # event_id is event's primary key (id)
        if event_id in user_events_ids:
            buttons.append(InlineKeyboardButton(f"{i+1} ✅ ", callback_data=f"sub_{event_id}"))
        else:
            buttons.append(InlineKeyboardButton(i+1, callback_data=f"sub_{event_id}"))

    buttons.append(InlineKeyboardButton(">", callback_data=f"page_up"))
    keyboard.add(*buttons)

    return keyboard


def get_unsubscribe_keyboard(obj_id, language='ua'):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(
        DICTIONARY[language]['unsubscribe_btn'],
        callback_data=f"unsubscribe_{obj_id}")
    )
    return keyboard


def get_admin_menu_keyboard(language='ua'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['support_btn'], DICTIONARY[language]['clear_events_btn'])
    keyboard.add(DICTIONARY[language]['add_admin_btn'], DICTIONARY[language]['delete_admin_btn'])
    keyboard.add(DICTIONARY[language]['settings_btn'], DICTIONARY[language]['mainmenu_msg'])
    return keyboard


def get_admin_settings_keyboard(language='ua'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        DICTIONARY[language]['settings_city_btn'],
        DICTIONARY[language]['settings_categories_btn'],
    )
    keyboard.add(DICTIONARY[language]['back_btn'])
    return keyboard


def get_admin_support_request_keyboard(obj_id, language='ua'):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(InlineKeyboardButton(
        DICTIONARY[language]['admin_respond_btn'],
        callback_data=f"respond_{obj_id}")
    )
    return keyboard


def get_skip_keyboard(language='ua'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['skip_btn'])
    return keyboard


def get_back_keyboard(language='ua'):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(DICTIONARY[language]['back_btn'])
    return keyboard
