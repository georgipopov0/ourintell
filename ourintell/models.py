from sqlalchemy import Column, Integer, String, Boolean
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_login import UserMixin
from flask import current_app

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
    is_verified = Column(Boolean, nullable = False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_verification_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


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