from netaddr import IPAddress, IPNetwork, AddrFormatError

from flask import url_for
from flask_mail import Message

from ourintell import mail

from ourintell.models import Subscription

def send_email(subscrition, event):
    user = subscrition.user
    message = Message('Ourintell Subscription update',
                  sender='georgipopov069@gmail.com',
                  recipients=[subscrition.ticketingAddress])

    message.body = f'''An event has been detected for your subscription:
{url_for('intell.getEvent', eventId = event.eventId, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message)

def send_discord_message(subscription, event):
    pass


ticketing_methods = {'email': send_email,
                    'discord': send_discord_message}

def check_network(subscrition, event):
    event = event.asDict()
    try:
        is_in_network = (IPAddress(event['eventData'].get('source.ip')) in IPNetwork(subscrition.trackedResource))
    except AddrFormatError:
        return False 
    return is_in_network


def check_url(subscrition, event):
    return False

type_handlers = {'network':check_network,
                'url':check_url}


def ticket_handler(event):
    subscritions = Subscription.query.all()
    for subscrition in subscritions:
        send_ticket = type_handlers[subscrition.trackedResourceType](subscrition, event)
        if(send_ticket):
            ticketing_methods[subscrition.ticketingMethod](subscrition, event)