from flask import request, Blueprint, jsonify, render_template, url_for

from  flask import current_app
from ourintell.models import RecordedEvents
from ourintell import db
from sqlalchemy import exc

import json 
from hashlib import sha256

intell = Blueprint('intell',__name__)

@intell.route("/")
@intell.route("/events", methods = ["GET"])
def getEvents():
    page = request.args.get("page", 1, type=int)
    eventsRaw= RecordedEvents.query.paginate(page=page, per_page=5)
    events = [i.asDict() for i in eventsRaw.items]

    return render_template('events.html', events = events)

@intell.route("/events", methods = ["POST"])
def addEvent():

    event = json.dumps(request.get_json())
    hashedEvent = sha256(event.encode('utf-8')).hexdigest()
    newEventEntry = RecordedEvents(hashedEvent,event)

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

    print(eventId)
    event = RecordedEvents.query.filter_by(eventId = eventId).first()
    event = json.loads(event.eventData)
    return render_template("event.html",event = event)



