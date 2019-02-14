from flask import Flask, Blueprint
import psycopg2

from api.v1 import v1
from api.models.errors import DBError

app = Flask(__name__)

def connect_to_db():
    try:    
        print(app.config.get("DATABASE"))
        connection = psycopg2.connect(**app.config.get("DATABASE"))
        return connection
    except Exception as error:
        raise DBError('could not establish a database connection')

def init_db():
    create_table_queries = []
    create_office_table = """CREATE TABLE IF NOT EXISTS political_office(
        id serial PRIMARY KEY,
        name VARCHAR (50) UNIQUE NOT NULL,
        office_type VARCHAR (50) NOT NULL
        );"""
    create_table_queries.append(create_office_table)

    create_party_table = """CREATE TABLE IF NOT EXISTS political_party(
        id serial PRIMARY KEY,
        name VARCHAR (50) UNIQUE NOT NULL,
        hq VARCHAR (50) UNIQUE NOT NULL,
        logo_url VARCHAR (50)
        );"""
    create_table_queries.append(create_party_table)

    con = connect_to_db()
    cur = con.cursor()

    for query in create_table_queries:
        cur.execute(query)
    con.commit()


def destroy_db():
    drop_table_queries = []

    drop_office_table = """ DROP TABLE IF EXISTS political_office """
    drop_table_queries.append(drop_office_table)

    drop_party_table = """ DROP TABLE IF EXISTS political_party """
    drop_table_queries.append(drop_party_table)

    con = connect_to_db()
    cur = con.cursor()

    for query in drop_table_queries:
        cur.execute(query)
    con.commit()




def create_app(configuration='config.Default'):
    app.config.from_object(configuration)
    connect_to_db()
    init_db()
    app.register_blueprint(v1)
    return app

    

