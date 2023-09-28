# Module for handling files for the data fetched from https://alquran.cloud
# Author: arenodi

# import module for handling data fetching
import quran_data_handler

# import os lib for path handling
import os

# import dump from json lib to write json obj to file
from json import dump


# function to generate a JSON file for an edition type
# requires a dictionary as argument
def generate_raw_file(identifier, edition_name):
    # file name based on the value of the arguments
    filename = f"raw_{edition_name}_{identifier}.json"
    # filepath for storing the raw data json file
    filepath = os.getcwd() + "\\raw_data"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    # Writing json file
    with open(f"{filepath}/{filename}", "w") as outfile:
        # serializing object as json
        dump(quran_data_handler.get_edition(identifier), outfile)

    return filepath + "\\" + filename


def generate_parsed_file(identifier, edition_name, edition_content):
    # file name based on the value of the arguments
    filename = f"parsed_{edition_name}_{identifier}.json"
    # filepath for storing the parsed quran data to new json file
    filepath = os.getcwd() + "\\parsed_data"
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    # Writing json file
    with open(f"{filepath}/{filename}", "w") as outfile:
        # serializing object as json
        dump(edition_content, outfile)
