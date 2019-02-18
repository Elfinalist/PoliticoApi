from flask import Flask, Blueprint
from api.database import Database
from api.v2 import v2
from api.models.errors import DBError, ConfigError


def create_app(configuration='config.Default'):
    app = Flask(__name__)
    app.config.from_object(configuration)
    database = Database(app.config.get("DATABASE"))
    database.init_db()
    app.register_blueprint(v2)
    return app
