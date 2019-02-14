import pytest
import flask

from api import create_app
from api.database import Database
from api.models.errors import ConfigError

@pytest.fixture
def app():
    try:
        app = create_app('config.TestingConfig')
        return app
    except ConfigError as error:
        print(error.message)
        raise SystemExit

@pytest.yield_fixture(scope="session")
def clear_db():
    yield
    Database.destroy_db()
