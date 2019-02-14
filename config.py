import os
from dotenv import load_dotenv
from api.models.errors import ConfigError

load_dotenv('.env')

def get_db_config():
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    if(database is None):
        raise ConfigError('config is missing DB_NAME environment variable')

    if(user is None):
        raise ConfigError('config is missing DB_USER environment variable')

    if(password is None):
        raise ConfigError('config is missing DB_PASSWORD environment variable')

    if(host is None):
        raise ConfigError('config is missing DB_HOST environment variable')
    
    if(port is None):
        raise ConfigError('config is missing DB_PORT environment variable')

    db = {
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "database": database
    }

    return db


class Default(object):
    DEBUG = False
    TESTING = False
    DATABASE = get_db_config()

class TestingConfig(object):
    TESTING = True
    DATABASE = {
        "user": "postgres",
        "password": "",
        "host": "localhost",
        "port": "5432",
        "database": "test_politico"
    }


