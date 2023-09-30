# Script to insert data to db
# Author: arenodi

# Import OS for handling the Json files
import os

# import load from json lib to  open json file to python obj
from json import load

# Module for handling the quran db
import quran_db_handler


# connect to database and get the connection obj
connection = quran_db_handler.db_connect()
# get cursor
cursor = connection.cursor()

db_name = "quran_json"

# delete db if exists, holds bool value
delete_db = quran_db_handler.db_delete_json(db_name, cursor)

# if delete successfully
if delete_db:
    # setup db successfully, holds bool value
    setup = quran_db_handler.db_setup_json(db_name, cursor)

    # if setup is True
    if setup:
        print("Data base setup successfully")
        directory = os.getcwd() + "/parsed_data"
        populate = quran_db_handler.populate_db(db_name, cursor, directory)
        if populate:
            print("Database populated successfully!")


connection.commit()

connection.close()
