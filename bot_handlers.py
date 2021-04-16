from bot_object import bot
from models import User
from database import session
from state_handler import get_state_and_process


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


if __name__ == '__main__':
    # bot.remove_webhook()
    # sleep(1)
    bot.polling(none_stop=True)
