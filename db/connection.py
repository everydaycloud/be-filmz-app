from psycopg2 import pool
from db.config import load_db_config

# Load database configuration from database.ini
db_config = load_db_config()

# Create a database connection pool
_pool = pool.Pool(db_config)

def get_connection():
    # Get a connection from the pool
    connection = _pool.getconn()

    # Return the connection
    return connection