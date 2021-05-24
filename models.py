from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    first_name = Column('first_name', Text)
    last_name = Column('last_name', Text)
    username = Column('username', Text, nullable=False)
    city = Column(String(100))
    language = Column(String(5))
    state = Column('state', Text, nullable=False)
    created_at = Column('created_on', DateTime, default=datetime.now)
    last_updated = Column('last_updated', DateTime, default=datetime.now, onupdate=datetime.now)
    subscriptions = relationship("UserSubscription", cascade="all,delete", backref="user", lazy='dynamic')
    events = relationship("UserEvent", cascade="all,delete", lazy='dynamic')

    def __init__(self, user_id, username, first_name, last_name, state):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.state = state

    def __repr__(self):
        return f"<User(username='{self.username}')>"

    def __str__(self):
        return self.username


class UserSubscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text, nullable=False)
    tags = Column(ARRAY(String(64)), nullable=True)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return f"<UserSubscription(name='{self.name}')>"

    def __str__(self):
        return self.name


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    id_site = Column(Integer, unique=True)
    name = Column(Text)
    # date = Column(DateTime, nullable=True)
    date = Column(Text, nullable=True)
    price = Column(Text, nullable=True)
    type = Column(ARRAY(String(64)), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(ARRAY(String(64)), nullable=True)
    subscribed_users = relationship("UserEvent", cascade="all,delete", lazy='dynamic')

    @hybrid_property
    def url(self):
        return f'https://dou.ua/calendar/{self.id_site}/'

    def __str__(self):
        return self.id


class UserEvent(Base):
    __tablename__ = 'user_events'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey(Event.id))
    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id

    def __repr__(self):
        return f"<UserEvent(id='{self.id}')>"

    def __str__(self):
        return self.id


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
