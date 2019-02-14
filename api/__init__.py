from flask import Flask, Blueprint
from api.database import Database
from api.v1 import v1
from api.models.errors import DBError, ConfigError


def create_app(configuration='config.Default'):
    app = Flask(__name__)
    app.config.from_object(configuration)
    database = Database(app.config.get("DATABASE"))
    database.init_db()
    app.register_blueprint(v1)
    return app

    

