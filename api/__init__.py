from flask import Flask, Blueprint
from api.v2.database import Database
from api.v2 import v2
from api.v1 import v1
from api.v2.models.errors import ConfigError, InputError

def create_app(configuration='config.Default'):
    app = Flask(__name__)
    app.config.from_object(configuration)
    database = Database(app.config.get("DATABASE"))
    database.init_db()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app
