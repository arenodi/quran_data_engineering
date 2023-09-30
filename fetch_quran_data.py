# Script to get data from https://alquran.cloud/api
# Author: arenodi

# Library to handle the Extracting and Transforming of quran data
import quran_data_handler

# Set the api url for fetching quran types
types_api_url = "http://api.alquran.cloud/v1/edition/type"

# list containing all the edition types
edition_types = quran_data_handler.get_data(types_api_url)

# dictionary containing the editions and identifiers
edition_identifiers = quran_data_handler.get_identifiers(edition_types)

# dictionary containing the edition types and the filepath for the raw data
raw_editions = []

# generate raw data json files and stores
for edition_name, identifier in edition_identifiers.items():
    raw_filepath = quran_data_handler.generate_raw_file(identifier, edition_name)
    raw_current = {
        "name": edition_name,
        "identifier": identifier,
        "rawFilepath": raw_filepath,
    }
    raw_editions.append(raw_current)
    print(f"Raw JSON file generated for edition: {raw_current['name']}.")

for raw_edition in raw_editions:
    transformed_edition = quran_data_handler.quaran_transform(
        raw_edition["rawFilepath"]
    )
    quran_data_handler.generate_parsed_file(
        raw_edition["identifier"], raw_edition["name"], transformed_edition
    )
    print(f"Raw JSON file generated for edition: {raw_edition['identifier']}.")
