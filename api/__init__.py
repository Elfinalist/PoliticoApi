from flask import Flask, Blueprint
from api.v2.database import Database
from api.v2.views.authentication import v2_authentication
from api.v2.views.candidate import v2_candidate
from api.v2.views.vote import v2_vote
from api.v2.views.party import v2_party
from api.v2.views.office import v2_offices
from api.v1.views.office import v1_office
from api.v1.views.party import v1_parties
from api.v2.models.errors import ConfigError, InputError

def create_app(configuration='config.Default'):
    app = Flask(__name__)
    app.config.from_object(configuration)
    database = Database(app.config.get("DATABASE"))
    database.init_db()
    app.register_blueprint(v1_office)
    app.register_blueprint(v1_parties)
    app.register_blueprint(v2_authentication)
    app.register_blueprint(v2_offices)
    app.register_blueprint(v2_party)
    app.register_blueprint(v2_candidate)
    app.register_blueprint(v2_vote)
    return app
