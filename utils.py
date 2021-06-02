from datetime import datetime
from logging import Logger

from database import session
from models import User, UserSubscription, Event, UserEvent, SupportRequest


def get_events_from_db_for_user(user):
    """Return events from db filtered by user settings"""
    user_event_types = ['Online', user.city] if user.city else ['Online']

    # user_subscriptions = session.query(UserSubscription.name).filter_by(user_id=user.id).all()
    # user_subscriptions = [i for sub in user_subscriptions for i in sub]
    user_subscriptions = [s.name for s in user.subscriptions.all()]

    # TODO: return all events so we can make pagination (now we limit events to 5 objects)
    events = session.query(Event).filter(
        Event.type.overlap(user_event_types),
        Event.tags.overlap(user_subscriptions)
    ).limit(5).all()

    return events


def get_events_for_user(user):
    """Return events from db on which user is subscribed"""
    user_events_id = session.query(UserEvent.event_id).filter_by(user_id=user.id).all()
    user_events_id = [i for obj in user_events_id for i in obj]
    events = session.query(Event).filter(
        Event.id.in_(user_events_id)
    ).all()
    # [event for event in user.events.all()]
    return events


def get_support_requests():
    """Return first five unresolved support request from db"""
    return session.query(SupportRequest).filter_by(is_resolved=False).limit(5).all()


# def format_support_request_as_msg(obj):
#     message = f""


def format_events_as_message(events):
    message = ""
    if isinstance(events, list):
        for event in events:
            message = f"*{event.name}*\n{event.date}"
            if event.price:
                message += f", {event.price}\n"
            message += f"\n_{event.description}_\n[Подробнее..]({event.url})\n\n"
    else:
        event = events
        message = f"*{event.name}*\n{event.date}"
        if event.price:
            message += f", {event.price}\n"
        message += f"\n_{event.description}_\n[Подробнее..]({event.url})\n\n"

    return message


def log_time(logger: Logger, msg):
    def log(func):
        def wrapped(*args, **kwargs):
            logger.info(f'start {msg}')
            t1 = datetime.now()
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                # capture_exception(e)
                logger.error(e, exc_info=True)
            t = datetime.now() - t1
            logger.info(f'{msg} took {t.seconds}s, {t.microseconds / 1000}ms')
            return result
        return wrapped
    return log
