import pathlib

BASE_DIR = pathlib.Path(__file__).parent

class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite///' + str(BASE_DIR / 'data' / 'db.sqlite3')
    QLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "flask_tutorial.sqlite3")
    SQLALCHEMY_TRACK_MODIDICATIONS = False