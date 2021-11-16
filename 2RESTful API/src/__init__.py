import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///D://Project\Flask\2RESTfulAPI\data\db.sqlite3'

db = SQLAlchemy(app)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from . import routes, models