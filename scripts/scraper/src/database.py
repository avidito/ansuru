import os
import psycopg2


HOSTNAME = os.environ.get("DB_HOSTNAME", "localhost")
DATABASE = os.environ.get("DB_DATABASE", "ansuru")
USERNAME = os.environ.get("DB_USERNAME", "ansuru")
PASSWORD = os.environ.get("DB_PASSWORD", "ansuru")
PORT     = os.environ.get("DB_PORT", "5432")

def get_cursor():
    conn = psycopg2.connect(
        host     = HOSTNAME,
        database = DATABASE,
        user     = USERNAME,
        password = PASSWORD,
        port     = PORT
    )
    cursor = conn.cursor()
    return conn, cursor
