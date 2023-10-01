# The making of 'Quran Data Engineering'

In this document, I will detail the thought process on making this application.

## About the challenge:

Here's what the challenge consisted of:

1. Write a Python script to call Quran API, fetching one edition for each type and storing it in a JSON file.
   
   * **Output:** Raw JSON files containing the Quran text in English translation with the following JSON structure:
     Edition
       |___ Juz
              |___ Surah

2. Write a Python script to read the raw JSON files and store the data in MariaDB.
   
   * **Output:** Data stored as json MariaDB tables.

3. Create materialized views in MariaDB that preserve the original architecture of the raw data.
   
   * **Output:** 5 Materialized views in MariaDB. One for each edition.

| Keys | Values    |
| ---- | --------- |
| Juz1 | ayah1...n |
| Juz2 | ayah2...n |

### First things first:

* I did not know anything about the Quran, so I had to research about it.

* I learned about the structure of the Quran, Juz, Surahs and Ayahs.

* I then studied the [Quran API](https://alquran.cloud/api) documentations, testing it out.

### Challenge Part 1: Http/get request -> Quran text -> JSON file

*Script: ~/fetch_quran_data.py* - [GitHub](https://github.com/arenodi/quran_data_engineering/blob/main/fetch_quran_data.py)

Following the Quaran API Docs, I noticed that the requests (depending on the endpoint) responses from a request would always bring the content in a *"data"* attribute. So I created a function called `get_data(url)` that would return a python object (`dict` or `list`) carrying the value of the attribute *"data"* .

The script works by first fetching the available types, returning a `list`. This `list` is passed to the `get_identifiers(types_list)` to be used in a for loop fetching the metadata of one Quran edition for every type in the list. The function returns a `dict` holding `{ edition_name: identifier , n }`.

A `for` loop is used to iterate over each `key, value` in the returned `dict`, passed as arguments to `generate_raw_file(identifier, edition_name)`. Within that, the value `identifier` is used for requesting the full Quran with the function`get_edition(identifier)`, this one returning a `dict` with the full Quran edition. The raw Quran `dict` is serialized as JSON formatted stream into a file and saved locally. At last, the `generate_raw_file` function returns the file path for the generated file. This file path is then added to dictionary `{"name": edition_name, "identifier": identifier, "rawFilepath": raw_filepath }}` and then appended to `raw_editions`.

Another `for`loop is used to iterate over each `dict` in `raw_editions`. The value of `rawFilepath` is passed to `quran_transform(filepath)` and the value of other keys is passed as argument to `generate_parsed_file(identifier, edition_name, edition_content)`.

Within `quran_transform()` the raw Quran file is deserialized as python `dict`, being iterated over with nested `for` loops to handle the intended restructuring. The function returns a new `dict` that is passed to `generate_parsed_file()`, to then be serialized as JSON formatted stream into a file.

### Challenge Part 2: JSON file -> MariaDB database

*Script: ~/db_insert_quran.py* - [GitHub](https://github.com/arenodi/quran_data_engineering/blob/main/db_insert_quran.py)

The script works by first establishing a connection using `db_connect()` that returns a connection object. The cursor is then referenced in `cursor` variable to be used for queries and other actions related to the database.

A database name referenced in `db_name`variable is used to create and perform operations in the database.

The first database operation is executed with `db_delete_json(database_name, cursor)` that deletes any database named as the name referenced by `db_name` returning a boolean value. If the first operation returns `True`, the second operation is executed with `db_setup_json(database_name, cursor)` that creates the database, the table, the columns to be used, and then returns a boolean value. If the second operation returns `True`, the `os` library is used to generate the path for the folder holding all the restructured JSON files. The third operation is executed with `populate_db(database_name, cursor, directory)`, where a for loop is used to open and read each file in `directory` path. Over each iteration the file content, referenced by `edition_json` is passed as argument to `json_to_jsondb(database_name, edition, edition_id, cursor)`, that handles the data insertion into the database table.

### Challenge Part 3: MariaDB database -> Views

*Script: ~/db_insert_quran.py* - [GitHub](https://github.com/arenodi/quran_data_engineering/blob/main/db_create_views.py)

This script's concept is simple. Is basically running the same SQL operation for each row in `editions` table.

It first establishes a connection with the database with `db_connect()` that returns a connection object. The cursor is then referenced in `cursor` variable to be used for queries and other actions related to the database.

The database name is also referenced in `db_name`variable and is used in query operations.

The `create_views(database_name, cursor)` is called, and within it the database is queried to get `edition_id` from every record in table `editions`. The result of the query is fetched into a `list` and referenced in `editions_id`. A for loop is used to iterate over each value in `editions_id` to execute a `CREATE VIEW...` command for every edition record. A *"View"* is created for each edition holding the values `juz_number, ayah_number, ayah_text`. The `create_views()` function returns a boolean value, that if `True` a success message is printed to the console.

### Thoughts

* With all this different functions created, I decided to organize the data fetching and transforming into a package called `quran_data_handler`, and all database related functions in a package called `quran_db_handler`.

* If you notice in `quran_db_handler`, there are functions like `db_setup()`and`json_to_structureddb()` and they are not being used. I created these functions as an alternative to a more traditional relational database.

* To make these scripts more autonomous, I would use `os.stdin, os.stdout`to pipe data triggering a chain of scripts.



The main python modules used are the following:

* `requests` for API requests.

* `mariadb`for database handling

* `os` for environment variables and path.

* `json` for serializing or deserializing JSON.
