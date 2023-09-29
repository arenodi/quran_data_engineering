FROM python:latest
WORKDIR /src/quran_api
RUN pip install requests mariadb
ENTRYPOINT [ "bash" ]