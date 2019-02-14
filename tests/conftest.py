import pytest

from api import create_app, destroy_db
from api.models.errors import ConfigError

@pytest.fixture
def app():
    try:
        app = create_app('config.TestingConfig')
        return app
    except ConfigError as error:
        print(error.message)
        raise SystemExit

@pytest.yield_fixture(autouse=True)
def clear_db():
    yield
    destroy_db()
