from database import session
from models import User, UserSubscription, Event


def get_events_from_db_for_user(user):
    user_event_types = ['Online', user.city] if user.city else ['Online']
    # print(f"\n{user_event_types=}")
    user_subscriptions = session.query(UserSubscription.name).filter_by(user_id=user.id).all()
    user_subscriptions = [i for sub in user_subscriptions for i in sub]
    # print(f"{user_subscriptions=}")

    # TODO: return all events so we can make pagination (now we limit events to 5 objects)
    events = session.query(Event).filter(
        Event.type.overlap(user_event_types),
        Event.tags.overlap(user_subscriptions)
    ).limit(5).all()

    return events


def format_events_as_message(events):
    message = ""

    for event in events:
        message += f"*{event.name}*\n" \
                   f"🕓 {event.date}\n"
        if event.price:
            message += f"{event.price}\n"

        message += f"\n_{event.description}_\n\n"

    return message
