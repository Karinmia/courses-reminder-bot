from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from enums import Languages, Roles
from database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    first_name = Column('first_name', Text)
    last_name = Column('last_name', Text)
    username = Column('username', Text)
    city = Column(String(100))
    language = Column(String(5), default='ua')
    role = Column(Enum(Roles), default=Roles.user.value)
    state = Column('state', Text)
    created_at = Column('created_at', DateTime, default=datetime.now)
    last_updated = Column('last_updated', DateTime, default=datetime.now, onupdate=datetime.now)
    subscriptions = relationship("UserSubscription", cascade="all,delete", backref="user", lazy='dynamic')
    events = relationship("UserEvent", cascade="all,delete", lazy='dynamic')
    support_requests = relationship("SupportRequest", cascade="all,delete", lazy='dynamic')

    # def __init__(self, username):
    #     self.username = username

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
    date = Column(Text, nullable=True)
    price = Column(Text, nullable=True)
    type = Column(ARRAY(String(64)), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(ARRAY(String(64)), nullable=True)
    subscribed_users = relationship("UserEvent", cascade="all,delete", lazy='dynamic')
    city = Column(Integer, ForeignKey('cities.id'))
    categories = relationship("EventCategory", cascade="all,delete", lazy='dynamic')

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


class SupportRequest(Base):
    __tablename__ = 'support_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    message = Column(Text, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column('created_at', DateTime, default=datetime.now)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f"<SupportRequest(id='{self.id}')>"

    def __str__(self):
        return self.id


class SupportResponse(Base):
    __tablename__ = 'support_responses'

    id = Column(Integer, primary_key=True)
    support_request_id = Column(Integer, ForeignKey(SupportRequest.id))
    message = Column(Text, nullable=False)

    def __init__(self, support_request_id, message):
        self.support_request_id = support_request_id
        self.message = message

    def __repr__(self):
        return f"<SupportRequest(id='{self.id}')>"

    def __str__(self):
        return self.id


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Category(id='{self.id}')>"

    def __str__(self):
        return self.name


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    is_regional_center = Column(Boolean, default=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<City(id='{self.id}')>"

    def __str__(self):
        return self.name


class EventCategory(Base):
    __tablename__ = 'event_categories'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey(Event.id))
    category_id = Column(Integer, ForeignKey(Category.id))

    def __init__(self, event_id, category_id):
        self.event_id = event_id
        self.category_id = category_id

    def __repr__(self):
        return f"<Category(id='{self.id}')>"

    def __str__(self):
        return self.name


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
