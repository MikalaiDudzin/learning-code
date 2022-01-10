import pathlib
import sqlite3

BASE_DIR = pathlib.Path(__file__).parent


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "flask_tutorial.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'you-will-never-know'
