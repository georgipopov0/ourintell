from flask import request, Blueprint, jsonify, render_template, url_for

from  flask import current_app
from ourintell.models import RecordedEvent
from ourintell import db
from sqlalchemy import exc

import json 
from hashlib import sha256

intell = Blueprint('intell',__name__)

@intell.route("/")
@intell.route("/events", methods = ["GET"])
def getEvents():
    page = request.args.get("page", 1, type=int)
    eventsRaw= RecordedEvent.query.paginate(page=page, per_page=5)
    events = [i.asDict() for i in eventsRaw.items]

    return render_template('events.html', events = events)

@intell.route("/events", methods = ["POST"])
def addEvent():

    event = json.dumps(request.get_json())
    hashedEvent = sha256(event.encode('utf-8')).hexdigest()
    newEventEntry = RecordedEvent(hashedEvent,event)

    db.session.add(newEventEntry)

    try:
        db.session.commit()
    except exc.IntegrityError as error:
        error_code = error.orig.args[0]
        if(error_code == 1062):
            return "value already exists", 409
        else:
            return 400

    return hashedEvent, 201

@intell.route('/event/<eventId>', methods = ["GET"])
def getEvent(eventId):

    event = RecordedEvent.query.filter_by(eventId = eventId).first()
    event = json.loads(event.eventData)
    return render_template("event.html",event = event)

@intell.route("/events/filtered", methods = ["GET"])
def getFilteredEvents():
    pageSize = 11
    tags =  request.args.copy()
    page = int(tags.pop('page', 1)) - 1
    eventsString = RecordedEvent.query.all()
    events = [i.asDict() for i in eventsString]
    filteredEvents = []
    for event in events:
        skipEvent = True 
        for tag in tags:
            if tag == 'page':
                continue
            if tags[tag] == "exists" and tag in event['eventData']:
                continue
            if event['eventData'].get(tag) != tags[tag]:
                skipEvent = False
                break
        if(skipEvent):
            filteredEvents.append(event)
    return render_template('events.html', events = filteredEvents[pageSize*page: pageSize*page+pageSize], tags = tags)

@intell.route("/test", methods = ["GET"])
def test():
    return request.args
