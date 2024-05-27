from dotenv import dotenv_values
import psycopg2


def connect_to_database():
    config = dotenv_values()
    try:
        # Establish the connection
        conn = psycopg2.connect(
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a test query
        cur.execute("SELECT version();")

        # Fetch the result
        db_version = cur.fetchone()
        print(f"Connected to PostgreSQL database, version: {db_version}")
        return conn

    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")


def close_connection(conn):
    # Close the cursor and connection
    cur = conn.cursor()
    cur.close()
    conn.close()
