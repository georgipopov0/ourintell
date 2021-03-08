from flask import url_for
from flask_mail import Message

from ourintell import mail

# Send a reset password email for  to the user
def send_reset_email(user):
    token = user.get_verification_token()
    message = Message('Password Reset Request',
                  sender='georgipopov069@gmail.com',
                  recipients=[user.email])

    message.body = f'''To reset your password, visit the following link:
{url_for('user.reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    try:
        mail.send(message)
    except:
        print(' not sent')

# Send a account verification email for  to the user
def send_accaunt_verification_email(user):
    token = user.get_verification_token()
    message = Message('Verify Account',
                  sender='georgipopov069@gmail.com',
                  recipients=[user.email])

    message.body = f'''To verify your account, visit the following link:
{url_for('user.verify_account', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    try:
        mail.send(message)
    except:
        print(' not sent')