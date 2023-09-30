#!/bin/bash

# executes python fetch data script
python fetch_quran_data.py

echo "Fetch Data Done."

# executes python insert data script
python db_insert_quran.py

echo "Insert Data Done."

# executes python create views
python db_create_views.py

echo "Create Views Done."