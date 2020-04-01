#!/usr/bin/env bash

# build spreading handler container
docker load -i setupEnvironment/dockerImages/python3_7_alpine.image
docker build -t spreading_handler.image -f setupEnvironment/dockerfiles/spreading_handler.dockerfile .
docker container create --name spreading_handler spreading_handler.image

# build rabbit mq container
docker load -i setupEnvironment/dockerImages/rabbitmq_management.image
docker build -t extended_rabbitmq_manageme.gitignorent.image -f setupEnvironment/dockerfiles/extended_rabbit_mq.dockerfile .
docker container create -p 5672:5672 -p 15672:15672 --name some-rabbit extended_rabbitmq_management.image

