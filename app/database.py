import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    db = os.environ.get("DATABASE")
    host = os.environ.get("HOST")
    user = os.environ.get("USER")
    password = os.environ.get("PASS")
    port = os.environ.get("PORT")
    
    return psycopg2.connect(
        database=db, 
        host=host, 
        user=user, 
        password=password, 
        port=port,
        cursor_factory=RealDictCursor
    )
