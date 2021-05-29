from flask import send_file,request, Blueprint, jsonify, render_template, url_for
import requests

import io
import csv

from  flask import current_app
from ourintell.models import RecordedEvent
from ourintell import db
from sqlalchemy import exc
from  ourintell.intell.utils import ticket_handler

import json 
from hashlib import sha256

intell = Blueprint('intell',__name__)

# This route is used for adding new events
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
            return 250

    # Check for subscriptions maching this event
    ticket_handler(newEventEntry)
    return 'Success', 201

@intell.route('/event/<eventId>', methods = ["GET"])
def get_event(eventId):

    event = RecordedEvent.query.filter_by(id = eventId).first()
    event = json.loads(event.event_data)
    return render_template("event.html",event = event)


@intell.route("/", methods = ["GET"])
@intell.route("/events", methods = ["GET"])
def get_events():
    pageSize = 11

    # Create a mutable dict containing the tags
    tags =  request.args.copy()

    # Pop the page argument
    page_string = tags.pop('page', 1)

    filteredEvents = RecordedEvent.get_filtered_events(tags)

    if(page_string == 'last'):
        page_string = len(filteredEvents)//pageSize
    if(page_string == 'first' ):
        page_string = 0
    
    page = int(page_string) - 1
    if page < 0:
        page = 0

    return render_template('events.html', events = filteredEvents[pageSize*page: pageSize*page+pageSize], tags = tags, current_page = page)

@intell.route("/download/events", methods = ["GET"])
def get_events_as_file():
    tags =  request.args.copy()
    if 'page' in tags:
        tags.pop('page')
    filteredEvents_raw = RecordedEvent.get_filtered_events(tags)
    filteredEvents = json.dumps([event['event_data'] for event in filteredEvents_raw])

    string_file = io.StringIO(filteredEvents)
    
    # Creating a bite object
    byte_file = io.BytesIO()
    byte_file.write(string_file.getvalue().encode())
    # Put the file pointer at 0
    byte_file.seek(0)
    string_file.close()

    # Return the created file
    return send_file(
        byte_file,
        as_attachment=True,
        attachment_filename='data.txt',
        mimetype='text/csv'
    )

@intell.route("/download/ip/events", methods = ["GET"])
def get_events_ip_as_file():
    tags =  request.args.copy()
    if 'page' in tags:
        tags.pop('page')
    filteredEvents_raw = RecordedEvent.get_filtered_events(tags)
    filteredEvents_ips = [event['event_data']['source.ip'] for event in filteredEvents_raw if 'source.ip' in event['event_data']]
    filteredEvents = json.dumps(filteredEvents_ips)

    string_file = io.StringIO(filteredEvents)
    
    # Creating a bite object
    byte_file = io.BytesIO()
    byte_file.write(string_file.getvalue().encode())
    # Puts the file pointer at 0
    byte_file.seek(0)
    string_file.close()

    # Return the created file
    return send_file(
        byte_file,
        as_attachment=True,
        attachment_filename='data.txt',
        mimetype='text/csv'
    )

@intell.route("/test", methods = ["GET"])
def test():
    return 'true'

@intell.route('/test_send', methods = ['GET'])
def test_send():
    test = requests.get('http://127.0.0.1:5000/test')
    return jsonify(test.text)