FROM mysql:9.3

COPY ../db/create_db.sql /docker-entrypoint-initdb.d/1_create_db.sql

EXPOSE 3306