# !/usr/bin/env

import pika

#
RMQ_IP = "10.100.102.41"

QUEUE0 = "queue_for_no_context"
QUEUE1 = "cA"
QUEUE2 = "cB"
QUEUES_DETAILS = [
    {"queue": QUEUE0, "routing_key": "0oka"},
    {"queue": QUEUE1, "routing_key": "1oka"},
    {"queue": QUEUE2, "routing_key": "2oka"}
]

EXCHANGE = "amq.topic"


def message_callback(ct, ch, method, properties, body):
    print(" [x] Received %r" % body)


class RabbitClient:

    def __init__(self):
        print("RMQ new instance")

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
        self.__declare_queues()

    def enqueue(self, routing_key, body):
        status = self.channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key, body=body)
        print(status)

    def basic_consume(self, queue, auto_ack=True, on_message_callback=message_callback, consumer_tag=""):
        self.channel.basic_consume(
            queue=queue,
            auto_ack=auto_ack,
            on_message_callback=on_message_callback,
            consumer_tag=consumer_tag
        )
        self.channel.start_consuming()

    def close_connection(self):
        print("closing connection")
        self.connection.close()

    def delete_all_queues(self):
        for index in range(len(QUEUES_DETAILS)):
            self.queue_delete(QUEUES_DETAILS[index]["queue"])

    def queue_delete(self, queue):
        self.channel.queue_delete(queue=queue)

    def __declare_queues(self):
        print("declaring queues")
        for index in range(len(QUEUES_DETAILS)):
            details = QUEUES_DETAILS[index]
            self.channel.queue_declare(queue=details["queue"], durable=True)
            self.channel.queue_bind(queue=details["queue"], exchange=EXCHANGE, routing_key=details["routing_key"])
