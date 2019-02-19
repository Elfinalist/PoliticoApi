import pytest

from api import create_app

@pytest.fixture
def app():
    app = create_app('config.TestingConfig')
    return app