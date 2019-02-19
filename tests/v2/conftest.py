import pytest

from api import create_app
from api.v2.database import Database
from api.v2.models.errors import ConfigError


@pytest.fixture
def app():
    try:
        app = create_app('config.TestingConfig')
        return app
    except ConfigError as error:
        print(error.message)
        raise SystemExit


@pytest.yield_fixture(scope="module", autouse=True)
def clear_db():
    yield
    Database.destroy_db()
