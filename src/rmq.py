# !/usr/bin/env python

import pika

from utils.utils import get_logger

# TODO: move all this props to CONFIG file which depends on environment variables (prod, dev, etc...)
RMQ_IP = "10.100.102.60"
RMQ_PORT = 5672
VIRTUAL_HOST = "/"
PERSISTENT_MODE = 2

QUEUE0 = "queue_for_no_context"
QUEUE1 = "cA"
QUEUE2 = "cB"
QUEUE3 = "cC"

QUEUES_DETAILS = [
    {"queue": QUEUE0, "routing_key": "0oka"},
    {"queue": QUEUE1, "routing_key": "1oka"},
    {"queue": QUEUE2, "routing_key": "2oka"},
    {"queue": QUEUE3, "routing_key": "3oka"},
]

EXCHANGE = "amq.topic"

LOGGER_NAME = 'rmq.logger'
logger = get_logger(LOGGER_NAME)


class RabbitClient:
    def __init__(self):
        logger.info("RMQ init new instance")

        self.connection = RabbitClient.get_connection()
        self.channel = self.connection.channel()
        self.__declare_queues()

        logger.info("turn on delivery confirmations...")

        # The basic rules of 'confirm_delivery' method are as follows:
        # 1) An un-routable mandatory or immediate message is confirmed right after the basic.return;
        # 2) A transient message is confirmed the moment it is enqueued
        # 3) A persistent message is confirmed when it is persisted to disk or when it is consumed on every queue
        # self.channel.confirm_delivery()

    def enqueue(self, routing_key, body):
        logger.info("trying enqueue a message with routing key: %s, and body: %s", routing_key, body)
        try:
            self.channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=PERSISTENT_MODE,
                )
            )
            logger.info("enqueue with routing_key: '%s', and body: '%s' was successful", routing_key, body)
            return True
        except pika.exceptions.UnroutableError as e:
            logger.error(
                "couldn't publish message. the error is: %s",
                routing_key,
                body,
                e.args[0].exception
            )
            return False

    def close_connection(self):
        logger.info("closing connection")
        self.connection.close()

    def delete_all_queues(self):
        logger.info("deleting all queues")
        for index in range(len(QUEUES_DETAILS)):
            self.queue_delete(QUEUES_DETAILS[index]["queue"])

    def queue_delete(self, queue):
        self.channel.queue_delete(queue=queue)

    def reset_state(self):
        try:
            self.delete_all_queues()
            self.__declare_queues()
        except pika.exceptions.ChannelClosedByBroker:
            logger.info("tried deleting queues, but queues are already deleted")

    def __declare_queues(self):
        logger.info("Declaring Queues")
        for index in range(len(QUEUES_DETAILS)):
            details = QUEUES_DETAILS[index]
            logger.info(
                "Declare a durable queue: '%s', and bind it to '%s' exchange with routing_key: '%s'",
                details["queue"],
                EXCHANGE,
                details["routing_key"]
            )
            self.channel.queue_declare(queue=details["queue"], durable=True)
            self.channel.queue_bind(queue=details["queue"], exchange=EXCHANGE, routing_key=details["routing_key"])

    @staticmethod
    def get_connection():
        credentials = pika.PlainCredentials(username="user", password="user")
        connection_params = pika.connection.ConnectionParameters(
            host=RMQ_IP,
            port=RMQ_PORT,
            virtual_host=VIRTUAL_HOST,
            credentials=credentials
        )

        logger.info("establishing tcp connection...")

        try:
            connection = pika.BlockingConnection(connection_params)
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("can't establish a tcp connection. error: '%s'", e.args[0])
            exit(-1)
        return connection
