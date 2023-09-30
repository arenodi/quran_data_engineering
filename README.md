# Quran Data

This is en ETL data piping application.



### Quick Overview

It works by retrieving data using the [Quran API](https://alquran.cloud/api) and transforming this data so that it can load into database, and also within the database generate views.



### Technologies Used

The following technologies are used in this project:

- Python 3.11.x

- MariaDB 11.x

- Docker 24.0.x
  
  

### Getting Started

1. To start using this application, first you need to fork it and the clone it in your machine.
2. Open a shell prompt in the main directory, or `cd` to the main directory from where is your current shell prompt.
3. Run `chmod +x runscript.sh`. This will give the file executable permissions.
4. Run `./runscript.sh` . This will setup everything needed for the application to work with docker:
   1.  Build the image from the Dockerfile in the folder named quran-api
   2. Create a docker network named quran-network
   3. Create a docker volume named quran-db
   4. Run a container as an instance of the mariadb image
   5. Run a container as an instance of the quran-api image that was built in step 4.1.
   
   Note: If you notice after running the `./runscript`, you will find yourself within the shell prompt of the quran-api container.
