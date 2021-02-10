from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_login import UserMixin
from flask import current_app

from ourintell import db, login_manager
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    is_verified = db.Column(db.Boolean, nullable = False)
    subscriptions = db.relationship('Subscription', backref = 'user', lazy=True)



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
    __tablename__ = 'recordedevents'
    eventId = db.Column(db.String(256), primary_key=True)
    eventData = db.Column(db.String(2047), nullable=False)

    def getEvent(self):
        return self.eventData

    def asDict(self):
        return{'eventId':self.eventId, 'eventData':json.loads( self.eventData)}

class TicketingMethod(db.Model):
    __tablename__ = 'ticketingmethods'
    ticketingMethod = db.Column(db.String(16), primary_key=True,)
    methodDescription = db.Column(db.String(32))
    # subscriptions = db.relationship('Subscription', backref = 'method', lazy=True)
    

class TrackableResource(db.Model):
    __tablename__ = 'trackableresources'
    resourceName = db.Column(db.String(16), primary_key=True, unique=True)
    # subscriptions = db.relationship('Subscription', backref = 'resource', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    Id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trackedResource = db.Column(db.String(16), db.ForeignKey('trackableresources.resourceName'), nullable=False)
    ticketingMethod = db.Column(db.String(16), db.ForeignKey('ticketingmethods.ticketingMethod'), nullable=False)
    ticketingAddress = db.Column(db.String(128), nullable=False)

# class UserSubscriptions(db.Model):
#     userId = db.Column(db.Integer, nullable=False)
#     subscriptionId = db.Column(db.Integer, nullable=False)

# class sentEvents(db.model):
#     eventId = db.Column(db.String(256), nullable=False)
#     subscriptionId = db.Column(db.Integer, nullable=False)