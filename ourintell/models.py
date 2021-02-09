from sqlalchemy import Column, Integer, String
from ourintell import db
from flask import current_app
import json

class RecordedEvent(db.Model):
    __tablename__ = 'RecordedEvents'
    eventId = Column(String(256), primary_key=True)
    eventData = Column(String(2047), nullable=False)

    def __init__(self, eventId=None, eventData=None):
        self.eventId = eventId
        self.eventData = eventData

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
