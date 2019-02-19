import psycopg2

from api.v2.models.errors import DBError, ConfigError


class Database(object):
    def __init__(self, db_config):
        global conn
        conn = self.connect_to_db(db_config)

    def connect_to_db(self, db_config):
        try:
            if(db_config.get("user") is None):
                raise ConfigError(
                    'config is missing DB_USER environment variable')

            if(db_config.get("password") is None):
                raise ConfigError(
                    'config is missing DB_PASSWORD environment variable')

            if(db_config.get("host") is None):
                raise ConfigError(
                    'config is missing DB_HOST environment variable')

            if(db_config.get("port") is None):
                raise ConfigError(
                    'config is missing DB_PORT environment variable')

            if(db_config.get("database") is None):
                raise ConfigError(
                    'config is missing DB_NAME environment variable')

            connection = psycopg2.connect(**db_config)
            return connection
        except Exception as error:
            if(isinstance(error, ConfigError)):
                print(error.message)
                raise SystemExit
            raise DBError('could not establish a database connection')

    def init_db(self):
        create_table_queries = []
        create_office_table = """CREATE TABLE IF NOT EXISTS political_office(
            id serial PRIMARY KEY,
            name VARCHAR (50) NOT NULL,
            office_type VARCHAR (50) NOT NULL
            );"""
        create_table_queries.append(create_office_table)

        create_party_table = """CREATE TABLE IF NOT EXISTS political_party(
            id serial PRIMARY KEY,
            name VARCHAR (50) NOT NULL,
            hq VARCHAR (50) NOT NULL,
            logo_url VARCHAR (50)
            );"""
        create_table_queries.append(create_party_table)

        create_user_table = """CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            name VARCHAR (100) NOT NULL,
            email VARCHAR (100) UNIQUE NOT NULL,
            password VARCHAR (100) NOT NULL,
            user_role SET DEFAULT "FALSE"
        );"""
        create_table_queries.append(create_user_table)
        cur = conn.cursor()

        for query in create_table_queries:
            cur.execute(query)
        conn.commit()

    @staticmethod
    def destroy_db():
        drop_table_queries = []

        drop_office_table = """ DROP TABLE IF EXISTS political_office """
        drop_table_queries.append(drop_office_table)

        drop_party_table = """ DROP TABLE IF EXISTS political_party """
        drop_table_queries.append(drop_party_table)

        drop_users_table = """ DROP TABLE IF EXISTS users """
        drop_table_queries.append(drop_users_table)

        cur = conn.cursor()

        for query in drop_table_queries:
            cur.execute(query)
        conn.commit()

    @staticmethod
    def get_connection():
        return conn
