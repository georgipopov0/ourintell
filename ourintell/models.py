from sqlalchemy import Column, Integer, String
from ourintell import db
from flask import current_app
import json

class RecordedEvent(db.Model):
    __tablename__ = 'RecordedEvents'
    eventId = Column(String(256), primary_key=True)
    eventData = Column(String(2047), nullable=False)

    def getEvent(self):
        return self.eventData

    def asDict(self):
        return{'eventId':self.eventId, 'eventData':json.loads( self.eventData)}

class User(db.Model):
    __tablename__ = "Users"
    userId = Column(Integer, primary_key = True)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class TicketingMethods(db.Model):
    ticketingMethod = Column(String(16), primary_key=True,)
    methodDescription = Column(String(32))

class TrackableResources(db.Model):
    resourceName = Column(String(16), primary_key=True, unique=True)

class Subscriptions(db.Model):
    subscriptionId = Column(Integer, primary_key=True, nullable=False)
    trackedResource = Column(String(128), nullable=False)
    trackingMethod = Column(String(16), nullable=False)
    trackedAddress = Column(String(128), nullable=False)
