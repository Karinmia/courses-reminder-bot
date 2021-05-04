from enums import CATEGORIES
from models import UserSubscription
from database import session


for categorie in CATEGORIES:
    session.add(UserSubscription(name=categorie))

session.commit()