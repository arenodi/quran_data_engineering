# Module to handle data fetching from https://alquran.cloud/api
# Author: arenodi

# Library to handle requests
import requests


# Function to handle get requests >>> returns a list
def get_data(url):
    # Try-except block to handle the response for types
    try:
        # variable to hold the response
        response = requests.get(url)
        # if status of response is 200 script will continue or else an exception will be thrown
        assert response.status_code == 200, (
            f"Status Code {response.status_code}.\n"
            + "Type data could not be fetched.\n"
        )
    except Exception as error:
        # Warns user of error
        print(error)
        # terminate the script
        exit()
    print(f"Data retrieve from -> '{url}'.")
    # returns the data attr from the response
    return response.json()["data"]


# function to get identifiers based on editions type list >>> returns a dictionary
def get_identifiers(type_list):
    # dictionary to hold the edition type and its identifier
    editions_identifiers = {}
    # Base url for english translated text editions
    editions_base_url = (
        "https://api.alquran.cloud/v1/edition?language=en&format=text&type=translation"
    )
    # get data from all the english translated text editions
    available_editions = get_data(editions_base_url)
    # try-except-finally block to retrieve data for each type and return dictionary with identifiers
    try:
        # if type_list is of type list and type_list has one or more items
        if (
            type(type_list) is list
            and len(type_list) > 0
            and type(available_editions) is list
        ):
            # iterate over the type_list list
            for current_index in range(len(type_list)):
                edition_name = available_editions[current_index]["name"].replace(
                    " ", "-"
                )
                identifier = available_editions[current_index]["identifier"]
                # append the identifier of the first ocurrence of the edition type
                editions_identifiers[edition_name] = identifier
        else:
            raise Exception("List of types is empty or is invalid")

    except Exception as error:
        print(error)

    finally:
        return editions_identifiers


# function to get the complete edition using an identifier as an argument
def get_edition(identifier):
    # variable holding the base url for fetching the full edition
    edition_base_url = "http://api.alquran.cloud/v1/quran/"
    # dictionary holding the full edition content
    edition_content = get_data(edition_base_url + identifier)
    print(f"Fetched edition: {identifier}")
    return edition_content
