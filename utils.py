from database import session
from models import User, UserSubscription, Event, UserEvent


def get_events_from_db_for_user(user):
    """Return events from db filtered by user settings"""
    user_event_types = ['Online', user.city] if user.city else ['Online']

    user_subscriptions = session.query(UserSubscription.name).filter_by(user_id=user.id).all()
    user_subscriptions = [i for sub in user_subscriptions for i in sub]

    # TODO: return all events so we can make pagination (now we limit events to 5 objects)
    events = session.query(Event).filter(
        Event.type.overlap(user_event_types),
        Event.tags.overlap(user_subscriptions)
    ).limit(5).all()

    return events


def get_events_for_user(user):
    """Return events from db on which user subscribed"""
    user_events_id = session.query(UserEvent.event_id).filter_by(user_id=user.id).all()
    user_events_id = [i for obj in user_events_id for i in obj]
    events = session.query(Event).filter(
        Event.id.in_(user_events_id)
    ).all()
    return events


def format_events_as_message(events):
    message = ""

    for i, event in enumerate(events):
        message += f"*{i+1}. {event.name}*\n{event.date}"
        if event.price:
            message += f", {event.price}\n"
        message += f"\n_{event.description}_\n[Подробнее..]({event.url})\n\n"

    return message
