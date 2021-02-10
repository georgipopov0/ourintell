import os

class Config:
    SECRET_KEY = os.getenv('ourintell_secret')
    SQLALCHEMY_DATABASE_URI =os.getenv('ourintell_database')