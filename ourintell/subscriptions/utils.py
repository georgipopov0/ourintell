from flask import url_for
from flask_mail import Message

from ourintell import mail

def send_verification_email(subscription):
    token = subscription.get_verification_token()
    message = Message('Verify Subscription',
                  sender='georgipopov069@gmail.com',
                  recipients=[subscription.ticketing_address])

    message.body = f'''To verify your subscription, visit the following link:
{url_for('subscriptions.verify_subscription', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    try:
        mail.send(message)
    except:
        print('not sent')


    def send_verification_discord_message(subscription):
        pass

    # This dict contains the relationship between the methods
    #  and the functions for their verification
    ticketing_methods = {'email': send_verification_email,
                        'discord': send_verification_discord_message}

    # Send a verification for the selected method
    def send_verification_token(subscription):
        ticketing_methods[subscription.thicketing_method](subscription)
