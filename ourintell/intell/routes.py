from flask import request, Blueprint, jsonify
from ourintell.models import RecordedEvents
from ourintell import db
from sqlalchemy import exc

import json 
from hashlib import sha256

intell = Blueprint('intell',__name__)

@intell.route("/")
def home():
    page = request.args.get("page",1,type=int)
    eventsRaw = RecordedEvents.query.paginate(page=page, per_page=5)
    events = jsonify([i.eventData for i in eventsRaw.items])
    return events

@intell.route("/test", methods = ["POST"])
def test():

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

@intell.route("/spas")
def spas():
    return "Spaasssssss"

