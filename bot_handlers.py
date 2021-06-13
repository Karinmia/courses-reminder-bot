import logging
from time import sleep

from bot_object import bot
from config import ADMINS, BOT_TOKEN
from database import session
from enums import Roles
from keyboards import *
from models import User, UserSubscription, Event, UserEvent, SupportRequest
from state_handler import get_state_and_process
from utils import get_events_from_db_for_user

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        logger.debug(f"/start | user_id: {message.from_user.id}")
        user = session.query(User).filter_by(user_id=message.from_user.id).first()

        role = Roles.user.value  # common user
        if str(message.from_user.id) in ADMINS:
            logger.info("ADMIN is here")
            role = Roles.user.admin

        if user is None:
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                state='set_language_state',
                role=role
            )
            session.add(user)
            session.commit()
        else:
            if not user.user_id:
                user.user_id = message.from_user.id
                user.first_name = message.from_user.first_name
                user.last_name = message.from_user.last_name
            else:
                user.state = 'main_menu_state'
            session.commit()

        get_state_and_process(message, user, True)
    except Exception as e:
        logger.error(e, exc_info=True)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user = session.query(User).filter_by(user_id=message.from_user.id).first()
        if user is None:
            user = User(user_id=message.from_user.id,
                        username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        last_name=message.from_user.last_name,
                        state='main_menu_state'
                        )
            session.commit()
        get_state_and_process(message, user)
    except Exception as e:
        logger.error(e, exc_info=True)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = session.query(User).filter_by(user_id=call.message.chat.id).first()

    if not call.message:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        user.state = 'main_menu_state'
        session.commit()
        get_state_and_process(call.message, user, True)

    if call.data == "save_categories":
        if user.state != 'settings_menu_state':
            user.state = 'set_city_state'
            session.commit()

        bot.send_message(
            call.message.chat.id,
            DICTIONARY[user.language]['saved_settings_msg']
        )
        get_state_and_process(call.message, user, True)

    elif call.data.startswith('sub_'):
        event_id = call.data.replace("sub_", "")
        # create UserEvent object and send message
        sub_event = session.query(UserEvent).filter_by(event_id=event_id, user_id=user.id).first()
        if not sub_event:
            sub_event = UserEvent(event_id=event_id, user_id=user.id)
            session.add(sub_event)
            session.commit()
            bot.send_message(
                call.message.chat.id,
                DICTIONARY[user.language]['subscribe_success_msg']
            )
            logger.debug(f'user {user.username} subscribed to event {event_id}')
        else:
            bot.send_message(
                call.message.chat.id,
                DICTIONARY[user.language]['already_subscribed_msg']
            )
        events = get_events_from_db_for_user(user)
        all_events_ids = [obj.id for obj in events]
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            call.message.message_id,
            reply_markup=events_inline_keyboard(all_events_ids, user)
        )
    elif call.data.startswith('unsubscribe_'):
        event_id = call.data.replace("unsubscribe_", "")
        # delete UserEvent object if it exists
        sub_event = session.query(UserEvent).filter_by(event_id=event_id, user_id=user.id).first()
        if sub_event:
            session.delete(sub_event)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            logger.error(e, exc_info=True)
        logger.error(f"Unsubscribed from event {event_id}")
        bot.send_message(
            call.message.chat.id,
            DICTIONARY[user.language]['unsubscribed_msg']
        )
        session.commit()
    elif call.data.startswith('category_'):
        sub_name = call.data.replace("category_", "")
        subscription = session.query(UserSubscription).filter_by(name=sub_name, user_id=user.id).first()
        if not subscription:
            subscription = UserSubscription(name=sub_name, user_id=user.id)
            session.add(subscription)
        else:
            session.delete(subscription)
        session.commit()
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            call.message.message_id,
            reply_markup=categories_inline_keyboard(user=user)
        )
    elif call.data.startswith('respond_'):
        sup_request_id = call.data.replace("respond_", "")
        sup_request = session.query(SupportRequest).filter_by(
            id=sup_request_id, is_resolved=False
        ).first()
        if not sup_request:
            logger.error(f"Can't find a support request with id {sup_request_id}")
            bot.send_message(
                call.message.chat.id,
                DICTIONARY[user.language]['already_subscribed_msg']
            )
        else:
            # create SupportResponse object
            user.state = 'send_support_respond_state'
            session.commit()
            get_state_and_process(call.message, user, True)
    else:
        logger.warning(f"Invalid call.data: {call.data}\nUser: id={user.id} username={user.username}")


def start_bot_handler():
    bot.remove_webhook()
    sleep(2)
    bot.set_webhook(url=f"https://course-helper-bot-kpi.herokuapp.com/{BOT_TOKEN}")
    # bot.polling(none_stop=True)


if __name__ == '__main__':
    start_bot_handler()