#!/bin/bash

# build image
docker build -t quran-api .
# create network
docker network create quran-network
# create volume
docker volume create quran-db
# run mariadb container detached
docker run -d --network quran-network --network-alias mariadb --mount type=volume,src=quran-db,target=/src/db_files -e MARIADB_ROOT_PASSWORD=adminpw mariadb
# run quran_api docker with bash as entrypoint
docker run -it --network quran-network --mount type=bind,src="$(pwd)",target=/src/quran_api -e MARIADB_HOST=mariadb -e MARIADB_USER=root -e MARIADB_PASSWORD=adminpw -e MARIA_DB=quran_data quran-api
