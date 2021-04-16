from sqlalchemy import Column, String, Integer, Boolean

from database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    first_name = Column('first_name', String(32))
    last_name = Column('last_name', String(32))
    username = Column('username', String(64))
    in_stock = Column('in_stock', Boolean)
    state = Column('state', String(64))

    def __init__(self, user_id, username, first_name, last_name, state):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.state = state


Base.metadata.create_all(engine)
