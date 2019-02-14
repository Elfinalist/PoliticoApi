import pytest

from api import create_app, destroy_db

@pytest.fixture
def app():
    app = create_app('config.TestingConfig')
    return app

@pytest.yield_fixture(autouse=True)
def clear_db():
    yield
    destroy_db()
