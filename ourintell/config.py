import os

class Config:
    SECRET_KEY = "spas"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/threat_data"