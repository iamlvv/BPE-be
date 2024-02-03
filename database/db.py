import psycopg2
import os
from urllib.parse import urlparse

HOST_DB_TEST = os.environ.get("HOST_DB_TEST")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")


class DatabaseConnector:
    connection = None
    # connection: psycopg2.connection

    @classmethod
    def get_connection(cls):
        if cls.connection is not None and cls.connection.closed == 0:
            print("Connected to the PostgreSQL database!")
            return cls.connection

        print("Connecting to the PostgreSQL database...")
        database_url = os.environ.get("DATABASE_URL")
        result = urlparse(database_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname

        cls.connection = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
        )
        return cls.connection
