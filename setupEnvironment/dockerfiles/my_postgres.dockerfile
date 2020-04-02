FROM postgres:9.6-alpine

ENV POSTGRES_USER user
ENV POSTGRES_PASSWORD user
ENV POSTGRES_DB spreader

# TODO: check how to make it run by default on docker create
# COPY setupEnvironment/utils/init_postgres.sql /docker-entrypoint-initdb.d/init_postgres.sql
