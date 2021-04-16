from database import session
from models import User
from states import *


states = {
    'login_state': login_state,
    'main_menu_state': main_menu_state,
}


def get_state_and_process(message, user: User, is_entry=False):
    print("--- in get_state_and_process()")
    if user.state in states:
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    else:
        user.state = 'main_menu_state'
        session.commit()
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    if change_state:
        print(change_state)
        go_to_state(message, state_to_change_name, user)


def go_to_state(message, state_name: str, user: User):
    print("--- in go_to_state()")
    user.state = state_name
    session.commit()
    get_state_and_process(message, user, is_entry=True)
