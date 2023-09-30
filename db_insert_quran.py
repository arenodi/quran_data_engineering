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

setup = quran_db_handler.db_setup("quran_data", cursor)

# if setup is True
if setup:
    print("Data base setup successfully")
    directory = os.getcwd() + "/parsed_data"
    try:
        # Edition id
        edition_id = 1
        # using the os.listdir function to iterate over the files in directory
        for json_file in os.listdir(directory):
            # loads file to python dict
            with open(f"{directory}/{json_file}") as parsed_quran:
                # dict to hold the data
                edition_dict = load(parsed_quran)

            # insert quran data into db
            insert_data = quran_db_handler.json_to_db(
                "quran_data", edition_dict, edition_id, cursor
            )
            if insert_data:
                print("Database populated successfully!")
                connection.commit()
            # increment edition id by one
            edition_id += 1

    except Exception as e:
        print(e)

connection.commit()

connection.close()
