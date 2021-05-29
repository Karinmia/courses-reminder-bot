from database import session
from models import User
from states import *


states = {
    'set_language_state': set_language_state,
    'login_state': login_state,
    'main_menu_state': main_menu_state,
    'set_city_state': set_city_state,
    'settings_menu_state': settings_menu_state,
    'change_city_state': change_city_state,
    'admin_menu_state': admin_menu_state,
}


def get_state_and_process(message, user: User, is_entry=False):
    if user.state in states:
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    else:
        user.state = 'main_menu_state'
        session.commit()
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    if change_state:
        go_to_state(message, state_to_change_name, user)


def go_to_state(message, state_name: str, user: User):
    user.state = state_name
    session.commit()
    get_state_and_process(message, user, is_entry=True)
