from flask import request, Blueprint, jsonify, render_template, url_for
import requests

from  flask import current_app
from ourintell.models import RecordedEvent
from ourintell import db
from sqlalchemy import exc
from  ourintell.intell.utils import ticket_handler

import json 
from hashlib import sha256

intell = Blueprint('intell',__name__)

@intell.route("/events", methods = ["POST"])
def add_event():

    event = json.dumps(request.get_json())
    hashedEvent = sha256(event.encode('utf-8')).hexdigest()
    newEventEntry = RecordedEvent(id=hashedEvent,event_data=event)
    
    db.session.add(newEventEntry)

    try:
        db.session.commit()
    except exc.IntegrityError as error:
        error_code = error.orig.args[0]
        if(error_code == 1062):
            return "value already exists", 409
        else:
            return 400

    ticket_handler(newEventEntry)
    return 'Success',201

@intell.route('/event/<eventId>', methods = ["GET"])
def get_event(eventId):

    event = RecordedEvent.query.filter_by(id = eventId).first()
    event = json.loads(event.event_data)
    return render_template("event.html",event = event)


@intell.route("/", methods = ["GET"])
@intell.route("/events", methods = ["GET"])
def get_events():
    pageSize = 11
    tags =  request.args.copy()
    page = int(tags.pop('page', 1)) - 1
    if page < 0:
        page = 0
    filteredEvents = RecordedEvent.get_filtered_events(tags)
    return render_template('events.html', events = filteredEvents[pageSize*page: pageSize*page+pageSize], tags = tags, current_page = page)

@intell.route("/test", methods = ["GET"])
def test():
    return 'true'

@intell.route('/test_send', methods = ['GET'])
def test_send():
    test = requests.get('http://127.0.0.1:5000/test')
    return jsonify(test.text)