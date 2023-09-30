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
   
   1. Build the image from the Dockerfile in the folder named quran-api
   2. Create a docker network named quran-network
   3. Create a docker volume named quran-db
   4. Run a container as an instance of the mariadb image
   5. Run a container as an instance of the quran-api image that was built in step 4.1.
   
   Note: If you notice after running the `./runscript`, you will find yourself within the shell prompt of the quran-api container.

##### Within the shell prompt of quran-api container:

1. Run `ls` to check if all files are present. The container uses a type bind mount.

2. Run `chmod +x quran_etl.sh`. This will give the file executable permissions

3. Run `./quran_etl.sh`. This will run all the scripts for the ETL data piping completion.

4. Now you exit the shell prompt by typing `exit` and pressing 'Enter'.

#### Entering the mariadb shell

    1. Run `docker exec -it <maria-db-container-id> mariadb -u root -p`. The password is `adminpw`.

    2. Now you can query the data from the table using `JSON_TABLE()` function or from the views just as any other table.



## Documentation


