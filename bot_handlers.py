from bot_object import bot
from models import User, UserSubscription
from database import session
from state_handler import get_state_and_process

from keyboards import *


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        print(f"/start | user_id: {message.from_user.id}")
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
        print(e)


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
        print(e)


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
    else:
        subscriptions = user.subscriptions.all()
        subscription = session.query(UserSubscription).filter(UserSubscription.name == call.data.replace("_on", "")).first()
        # subscriptions = UserSubscription(name=call.data.replace("_on", ""))
        if subscription in subscriptions:
            user.subscriptions.remove(subscription)
        else:
            user.subscriptions.append(subscription)
        session.commit()
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            call.message.message_id,
            reply_markup=categories_inline_keyboard(user=user)
        )
        # get_state_and_process(call.message, user, True)




if __name__ == '__main__':
    # bot.remove_webhook()
    # sleep(1)
    bot.polling(none_stop=True)
