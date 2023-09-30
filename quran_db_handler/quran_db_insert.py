# Module to insert data into the database
# Author: arenodi

# Import mariadb module
import mariadb

# import dumps from json lib to  serialize edition content
from json import dumps

# Module for handling the quran db
import quran_db_handler

# Import OS for handling the Json files
import os


def populate_db(database_name, cursor, directory):
    DID_WORK = True
    try:
        # Edition id
        edition_id = 1
        # using the os.listdir function to iterate over the files in directory
        for json_file in os.listdir(directory):
            # loads file to python dict
            with open(f"{directory}/{json_file}", "r") as parsed_quran:
                # dict to hold the data
                edition_json = (
                    parsed_quran.read().replace("'", "''").replace('\\"', '\\\\"')
                )
                parsed_quran.close()

            # insert quran data into db
            insert_data = quran_db_handler.json_to_jsondb(
                database_name, edition_json, edition_id, cursor
            )
            if insert_data:
                print(f"Edition {edition_id} inserted in table successfully!")
            # increment edition id by one
            edition_id += 1

    except Exception as e:
        print(e)
        DID_WORK = False

    return DID_WORK


# function to insert data from json to database:
def json_to_structureddb(database_name, edition, edition_id, cursor):
    # flag for operation success
    DID_WORK = True
    try:
        print(
            f"Trying to insert edition: {edition['identifier']} into {database_name} Database:"
        )
        # Select database
        cursor.execute(f"USE {database_name};")
        # Start data insertion in the editions table
        cursor.execute(
            f"INSERT INTO editions VALUES ({edition_id},'{edition['name']}','{edition['englishName']}','{edition['identifier']}','{edition['language']}','{edition['type']}');"
        )
        # iterate over all the juz
        for juz in edition["content"]:
            # juz_id string concatenation
            juz_id = str(str(edition_id) + "-" + str(juz["number"]))
            # insert into juz the current juz data
            cursor.execute(
                f"INSERT INTO juz VALUES ('{juz_id}',{juz['number']}, {edition_id});"
            )
            # iterate over the surahs
            for surah in juz["content"]:
                # surah_id string concatenation
                surah_id = str(edition_id) + "-" + str(surah["number"])
                # insert into surah the current surah data, here the query will use IGNORE for duplicate values
                cursor.execute(
                    f"INSERT IGNORE INTO surahs VALUES ('{surah_id}',{surah['number']}, '{surah['name']}',{edition_id});"
                )
                # iterate over the ayahs
                for ayah in surah["ayahs"]:
                    # surah_id string concatenation
                    ayah_id = (
                        str(edition_id)
                        + "-"
                        + juz_id
                        + "-"
                        + surah_id
                        + "-"
                        + str(ayah["number"])
                    )
                    # get ayah text and transform it to not occurr errors in mariadb
                    ayah_text = ayah["text"].replace("'", "''")
                    # insert ayah data into ayahs table
                    cursor.execute(
                        f"INSERT INTO ayahs VALUES ('{ayah_id}',{ayah['number']},'{ayah_text}', {edition_id}, '{juz_id}', '{surah_id}')"
                    )
    except mariadb.Error as e:
        print(e)
        DID_WORK = False

    return DID_WORK


# function to insert data from json to json database:
def json_to_jsondb(database_name, edition, edition_id, cursor):
    # flag for operation success
    DID_WORK = True
    # print(edition)
    try:
        print(f"Trying to insert edition with json data into {database_name} Database:")
        # Select database
        cursor.execute(f"USE {database_name};")
        # Start data insertion in the editions table
        cursor.execute(f"INSERT INTO editions VALUES ({edition_id},'{edition}');")
    except mariadb.Error as e:
        print(e)
        DID_WORK = False

    return DID_WORK
