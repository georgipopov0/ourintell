from sqlalchemy import Column, Integer, String
from flask_login import UserMixin

from ourintell import db, login_manager
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class RecordedEvent(db.Model):
    __tablename__ = 'RecordedEvents'
    eventId = Column(String(256), primary_key=True)
    eventData = Column(String(2047), nullable=False)

    def getEvent(self):
        return self.eventData

    def asDict(self):
        return{'eventId':self.eventId, 'eventData':json.loads( self.eventData)}

# class TicketingMethods(db.Model):
#     ticketingMethod = Column(String(16), primary_key=True,)
#     methodDescription = Column(String(32))

# class TrackableResources(db.Model):
#     resourceName = Column(String(16), primary_key=True, unique=True)

# class Subscriptions(db.Model):
#     subscriptionId = Column(Integer, primary_key=True, nullable=False)
#     trackedResource = Column(String(128), nullable=False)
#     trackingMethod = Column(String(16), nullable=False)
#     trackedAddress = Column(String(128), nullable=False)

# class UserSubscriptions(db.Model):
#     userId = Column(Integer, nullable=False)
#     subscriptionId = Column(Integer, nullable=False)

# class sentEvents(db.model):
#     eventId = Column(String(256), nullable=False)
#     subscriptionId = Column(Integer, nullable=False)