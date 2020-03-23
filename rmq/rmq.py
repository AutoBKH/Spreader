# !/usr/bin/env

import pika
from utils.utils import get_logger

RMQ_IP = "10.100.102.48"

QUEUE0 = "queue_for_no_context"
QUEUE1 = "cA"
QUEUE2 = "cB"
QUEUES_DETAILS = [
    {"queue": QUEUE0, "routing_key": "0oka"},
    {"queue": QUEUE1, "routing_key": "1oka"},
    {"queue": QUEUE2, "routing_key": "2oka"}
]

EXCHANGE = "amq.topic"

LOGGER_PATH = r'C:\Users\Shani Hochma\PycharmProjects\ShaniIsWorking\logs\rmq.logger'
LOGGER_NAME = 'rmq.logger'
logger = get_logger(LOGGER_NAME, LOGGER_PATH)


def message_callback(ct, ch, method, properties, body):
    logger.info(" [x] Received %r", body)


def do_nothing():
    pass


class RabbitClient:
    def __init__(self, on_ack=do_nothing, on_nack=do_nothing):
        logger.info("RMQ init new instance")

        credentials = pika.PlainCredentials("guest", "guest")
        connection_params = pika.connection.ConnectionParameters(
            host=RMQ_IP,
            port=5672,
            virtual_host="/",
            credentials=credentials
        )

        # establish tcp connection
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()
        # TODO: check how to add properly confirm_delivery
        # self.channel.confirm_delivery(
        #     ack_nack_callback=lambda frame: RabbitClient.__on_delivery_confirmation(frame, on_ack, on_nack)
        # )
        self.__declare_queues()

    def enqueue(self, routing_key, body):
        logger.info("enqueue message with routing key: %s, and body: %s", routing_key, body)
        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

    def basic_consume(self, queue, auto_ack=True, on_message_callback=message_callback, consumer_tag=""):
        logger.info("basic_consume")
        self.channel.basic_consume(
            queue=queue,
            auto_ack=auto_ack,
            on_message_callback=on_message_callback,
            consumer_tag=consumer_tag
        )
        self.channel.start_consuming()

    def close_connection(self):
        logger.info("closing connection")
        self.connection.close()

    def delete_all_queues(self):
        logger.info("deleting all queues")
        for index in range(len(QUEUES_DETAILS)):
            self.queue_delete(QUEUES_DETAILS[index]["queue"])

    def queue_delete(self, queue):
        self.channel.queue_delete(queue=queue)

    def __declare_queues(self):
        logger.info("Declaring Queues")
        for index in range(len(QUEUES_DETAILS)):
            details = QUEUES_DETAILS[index]
            logger.info(
                "Declare a durable queue: %s, and bind it to %s exchange with route: %s",
                details["queue"],
                EXCHANGE,
                details["routing_key"]
            )
            self.channel.queue_declare(queue=details["queue"], durable=True)
            self.channel.queue_bind(queue=details["queue"], exchange=EXCHANGE, routing_key=details["routing_key"])

    @staticmethod
    def __on_delivery_confirmation(frame, on_ack, on_nack):
        if isinstance(frame.method, pika.spec.Basic.Ack):
            logger.info('Received confirmation: %s', frame.method)
            on_ack()
        else:
            logger.error('Received negative confirmation: %s', frame.method)
            on_nack()
