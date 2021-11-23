from flask_migrate import Migrate
from flask_restful import Api
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
api = Api(app)
from . import routes , models

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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/greeting', methods=['POST'])
def greeting():
    name = request.form.get('name')
    if not name:
        return 'Please , enter a value', 400
    return render_template('greeting.html', name=name)