import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    db = os.environ.get("DATABASE")
    host = os.environ.get("HOST")
    user = os.environ.get("USER")
    password = os.environ.get("PASS")
    port = os.environ.get("PORT")
    url = os.environ.get("DATABASE_URL")

    # #gcp cloud sql connection
    # return psycopg2.connect(url, cursor_factory=RealDictCursor)

    unix_socket = '/cloudsql/{}'.format(host)
    return psycopg2.connect(database=db, user =user, password = password, host = unix_socket, cursor_factory=RealDictCursor)