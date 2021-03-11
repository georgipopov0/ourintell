from netaddr import IPAddress, IPNetwork, AddrFormatError

from flask import url_for
from flask_mail import Message

from ourintell import mail

from ourintell.models import Subscription

# Send email for subscription match subscription
def send_email(subscrition, event):
    user = subscrition.user
    message = Message('Ourintell Subscription update',
                  sender='georgipopov069@gmail.com',
                  recipients=[subscrition.ticketing_address])

    message.body = f'''An event has been detected for your subscription:
{url_for('intell.get_event', eventId = event.id, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    try:
        mail.send(message)
    except:
        print(' not sent')

def send_discord_message(subscription, event):
    pass

def send_api_message():
    pass


# Dict relating the ticketing method to the tiketing functions
ticketing_methods = {'email': send_email,
                    'discord': send_discord_message,
                    "API": send_api_message
                    }

# Check if an ip is in the given network
def check_network(subscrition, event):
    event = event.asDict()
    ip_string = event['event_data'].get('source.ip')
    if(not ip_string):
        return False
    try:
        ip = IPAddress(ip_string)
    except AddrFormatError:
        return False 
    is_in_network = ( ip in IPNetwork(subscrition.tracked_resource))
    return is_in_network

# Check for a domain match
def check_url(subscrition, event):
    return event.get("source.fqdn") == event.get(source.fqdn) 


# Dict relating the tracked resource 
# to check function for the method
type_handlers = {'network':check_network,
                'url':check_url}

# Loop trough all subscriptions and send a mesage 
# if an event matches the subscription parameters
def ticket_handler(event):
    subscritions = Subscription.query.all()
    for subscrition in subscritions:
        if(subscrition.is_verified is False):
            continue
        # Call the appropriate function from type_handlers to check for matching event 
        match_found = type_handlers[subscrition.tracked_resource_type](subscrition, event)
        if(match_found):
            # Send a message with the appropriate media
            ticketing_methods[subscrition.ticketing_method](subscrition, event)