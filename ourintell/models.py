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

    # Generate a verification token for the user
    def get_verification_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    # Get a user from a verification token
    @staticmethod
    def verify_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class RecordedEvent(db.Model):
    __tablename__ = 'recorded_events'
    id = db.Column(db.String(256), primary_key=True)
    event_data = db.Column(db.String(2047), nullable=False)

    def get_event(self):
        return self.event_data

    def asDict(self):
        return{'id':self.id, 'event_data':json.loads( self.event_data)}

    # Filter all events by tag
    @staticmethod
    def get_filtered_events(tags):
        events_string = RecordedEvent.query.all()
        # convert all events to dicts
        events = [i.asDict() for i in events_string]
        filteredEvents = []
        for event in events:
            skipedEvent = False
            for tag in tags:
                # Check if an event has a given key  
                if tags[tag] == "exists" and tag in event['event_data']:
                    continue
                # Check if the event matches all tags and skis it on a missmach
                if event['event_data'].get(tag) != tags[tag]:
                    skipedEvent = True
                    break

            # Check if the event has been skipped
            if(not skipedEvent):
                filteredEvents.append(event)
        return filteredEvents

class TicketingMethod(db.Model):
    __tablename__ = 'ticketing_methods'
    method = db.Column(db.String(16), primary_key=True,)
    

class TrackableResourceType(db.Model):
    __tablename__ = 'trackable_resource_types'
    resource_type = db.Column(db.String(16), primary_key=True, unique=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False)
    tracked_resource = db.Column(db.String, nullable=False)
    tracked_resource_type = db.Column(db.String(16), db.ForeignKey('trackable_resource_types.resource_type'), nullable=False)
    ticketing_method = db.Column(db.String(16), db.ForeignKey('ticketing_methods.method'), nullable=False)
    ticketing_address = db.Column(db.String(128), nullable=False)

    sent_tickets = db.relationship('Sent_ticket', backref = 'subscription', lazy=True)

    # Generate a verification token
    def get_verification_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'subscription_id': self.id}).decode('utf-8')

    # Retrun a subscription from verification token
    @staticmethod
    def verify_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            subscription_id = serializer.loads(token)['subscription_id']
        except:
            return None
        return Subscription.query.get(subscription_id)


class Sent_ticket(db.Model):
    __tablename__ = 'sent_tickets'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    subscriptionId = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    eventId = db.Column(db.String, db.ForeignKey('recorded_events.id'),nullable=False)