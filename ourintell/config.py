import os

class Config:
    # Get the variables from the environment
    SECRET_KEY = os.getenv('OURINTELL_SECRET')
    MAIL_USERNAME = os.getenv('OURINTELL_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('OURINTELL_MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.getenv('OURINTELL_DATABASE')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

