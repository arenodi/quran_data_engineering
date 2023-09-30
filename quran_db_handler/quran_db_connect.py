# Module to connect to the database
# Author: arenodi

# Import mariadb module
import mariadb

# OS module for handling enviroment variables
import os


# function to connect to database
def db_connect():
    # Connect to mariadb instance container
    try:
        conn = mariadb.connect(
            user=os.getenv("MARIADB_USER"),
            password=os.getenv("MARIADB_PASSWORD"),
            host=os.getenv("MARIADB_HOST"),
            port=3306,
            database=os.getenv("MARIADB_DB"),
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(1)

    # return cursor
    return conn
