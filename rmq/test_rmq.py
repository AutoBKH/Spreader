# !/usr/bin/env

import pytest

from rmq.rmq import RabbitClient, QUEUES_DETAILS

FIRST_MESSAGE = b"1111this is my first message!1111"
SECOND_MESSAGE = b"2222this is my second message!2222"


@pytest.fixture(name='rabbit')
def init_queue():
    return RabbitClient()


def test_rmq_client(rabbit):

    # ensures no data in queues from previous tests
    rabbit.reset_state()

    # insert queues
    status = rabbit.enqueue(routing_key=QUEUES_DETAILS[0]["routing_key"], body=FIRST_MESSAGE)
    assert status is True
    status = rabbit.enqueue(routing_key=QUEUES_DETAILS[1]["routing_key"], body=SECOND_MESSAGE)
    assert status is True

    # consume queues0
    connection1 = rabbit.get_connection()
    channel1 = connection1.channel()
    channel1.basic_consume(
        queue=QUEUES_DETAILS[0]["queue"],
        on_message_callback=first_message_callback
    )
    connection1.close()

    # consume queues1
    connection2 = rabbit.get_connection()
    channel2 = connection2.channel()
    channel2.basic_consume(
        queue=QUEUES_DETAILS[1]["queue"],
        on_message_callback=second_message_callback
    )
    channel2.start_consuming()
    connection2.close()

    # reset state at the end of the test
    rabbit.delete_all_queues()
    rabbit.close_connection()


# helping functions
def first_message_callback(ch, method, properties, body):
    ch.stop_consuming()
    assert body == FIRST_MESSAGE


def second_message_callback(ch, method, properties, body):
    ch.stop_consuming()
    assert body == SECOND_MESSAGE
