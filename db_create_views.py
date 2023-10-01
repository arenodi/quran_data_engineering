# Script to insert data to db
# Author: arenodi

# Module for handling the quran db
import quran_db_handler


# connect to database and get the connection obj
connection = quran_db_handler.db_connect()
# get cursor
cursor = connection.cursor()

db_name = "quran_json"

view_create = quran_db_handler.create_views(db_name, cursor)

if view_create:
    print("Create Views Successfully!")
