import logging

from bot_object import bot
from database import session
from keyboards import *
from models import User, UserSubscription, Event, UserEvent
from state_handler import get_state_and_process

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        logger.debug(f"/start | user_id: {message.from_user.id}")
        user = session.query(User).filter_by(user_id=message.from_user.id).first()

        if user is None:
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                state='login_state'
            )
            session.add(user)
            session.commit()
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
        user.state = 'set_city_state'
        session.commit()
        get_state_and_process(call.message, user, True)
    elif call.data.startswith('sub_'):
        event_id = call.data.replace("sub_", "")
        # create UserEvent object and send message
        try:
            sub_event = UserEvent(event_id=event_id, user_id=user.id)
            session.add(sub_event)
            session.commit()
        except Exception as e:
            logger.error(e)
            bot.send_message(
                call.message.chat.id,
                text="Вы уже подписались на это событие"
            )
        else:
            logger.debug(f'user {user.username} subscribed to event {event_id}')
            bot.send_message(
                call.message.chat.id,
                text="Вы успешно подписались на событие! Мы напомним о нем за день до начала."
            )
    else:
        sub_name = call.data.replace("_on", "")
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
        # get_state_and_process(call.message, user, True)


def start_bot_handler():
    # bot.remove_webhook()
    # sleep(1)
    bot.polling(none_stop=True)


if __name__ == '__main__':
    # bot.remove_webhook()
    # sleep(1)
    bot.polling(none_stop=True)
