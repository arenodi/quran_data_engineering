# Module to setup the database
# Author: arenodi

# Import mariadb module
import mariadb


# function to setup the database
def db_setup(database_name, cursor):
    # Flag to return success of database setup
    DID_WORK = True
    # try-except block
    try:
        # create the database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
        # Select database
        cursor.execute(f"USE {database_name};")
        try:
            # Create editions table
            cursor.execute(
                """CREATE TABLE editions(edition_id int not null,
                        name varchar(30) not null,
                        english_name varchar(30) not null,
                        identifier varchar(25) not null,
                        language varchar(2) not null,
                        type varchar(12),
                        primary key(edition_id));"""
            )
        except mariadb.Error as e:
            print(f"Error in create editions: {e}")
            raise TypeError("Error in the CREATE TABLE editions() step.")
        # create juz table with foreign key referencing to editions
        cursor.execute(
            """CREATE TABLE juz(juz_id varchar(10) not null, 
                        juz_number int not null,
                        edition_id int not null,
                        primary key(juz_id),
                        foreign key(edition_id) references editions(edition_id));"""
        )
        # create surahs table with foreign key referencing to editions
        cursor.execute(
            """CREATE TABLE surahs( surah_id varchar(8) not null,
                        surah_number int not null,
                        name varchar(100) not null,
                        edition_id int not null,
                        primary key(surah_id),
                        foreign key(edition_id) references editions(edition_id));"""
        )
        # create ayahs table with foreign keys referencing to editions, juz and surahs
        cursor.execute(
            """CREATE TABLE ayahs(ayah_id varchar(20) not null,
                        ayah_number int not null,
                        text varchar(2000) not null,
                        edition_id int not null,
                        juz_id varchar(6) not null,
                        surah_id varchar(8) not null,
                        primary key(ayah_id),
                        foreign key(edition_id) references editions(edition_id),
                        foreign key(juz_id) references juz(juz_id),
                        foreign key(surah_id) references surahs(surah_id));"""
        )
    # handling error
    except (mariadb.Error, TypeError) as error:
        print(f"Error: {error}")
        # Flag false
        DID_WORK = False
    # return boolean value
    return DID_WORK


# function to setup json formatted db
def db_setup_json(database_name, cursor):
    # Flag to return success of database setup
    DID_WORK = True
    # try-except block
    try:
        # create the database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
        # Select database
        cursor.execute(f"USE {database_name};")
        try:
            # Create editions table
            cursor.execute(
                """CREATE TABLE editions(edition_id int not null,
                        edition LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
                        CHECK (JSON_VALID(`edition`)),
                        primary key(edition_id));"""
            )
        except mariadb.Error as e:
            print(f"Error in create editions: {e}")
            raise TypeError("Error in the CREATE TABLE editions() step.")
    # handling error
    except (mariadb.Error, TypeError) as error:
        print(f"Error: {error}")
        # Flag false
        DID_WORK = False
    # return boolean value
    return DID_WORK
