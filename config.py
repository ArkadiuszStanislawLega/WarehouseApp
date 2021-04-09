import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
DB_NAME = 'mag_app.db'


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
