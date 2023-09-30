# Module to setup the database
# Author: arenodi

# Import mariadb module
import mariadb


# function to setup the database
def db_delete(database_name, cursor):
    # Flag to return success of database setup
    DID_WORK = True
    try:
        # Select database
        cursor.execute(f"USE {database_name};")
        # truncate table ayahs
        truncate_table("ayahs", cursor)
        # deletes ayahs table
        cursor.execute("DROP TABLE IF EXISTS ayahs;")
        # truncate table ayahs
        truncate_table("surahs", cursor)
        # deletes ayahs table
        cursor.execute("DROP TABLE IF EXISTS surahs;")
        # truncate table ayahs
        truncate_table("juz", cursor)
        # deletes ayahs table
        cursor.execute("DROP TABLE IF EXISTS juz;")
        # truncate table ayahs
        truncate_table("editions", cursor)
        # deletes ayahs table
        cursor.execute("DROP TABLE IF EXISTS editions;")
        # deletes ayahs table
        cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")

    except mariadb.Error as e:
        print(f"Error: {e}")
        DID_WORK = False

    return DID_WORK


# function to setup the database
def db_delete_json(database_name, cursor):
    # Flag to return success of database setup
    DID_WORK = True
    try:
        # deletes editions table
        cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")

    except mariadb.Error as e:
        print(f"Error: {e}")
        DID_WORK = False

    return DID_WORK


# function to truncate a table
def truncate_table(table_name, cursor):
    # Flag to return success of operation
    DID_WORK = True
    try:
        # executes truncate table command
        cursor.execute(f"TRUNCATE TABLE {table_name}")
    except mariadb.Error as e:
        print(f"Was not possible to truncate table.\n{e}")
        DID_WORK = False
    return DID_WORK
