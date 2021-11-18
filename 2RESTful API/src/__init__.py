from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
import os
from . import routes, models
import  config

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///D://Project\Flask\2RESTfulAPI\data\db.sqlite3'
app.config.from_object(config.Config)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
migrate = Migrate(app,db)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Flask tutorial'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
