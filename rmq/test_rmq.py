# !/usr/bin/env

import pytest

from rmq.rmq import RabbitClient, QUEUES_DETAILS

FIRST_MESSAGE = b"1111this is my first message!1111"
SECOND_MESSAGE = b"2222this is my second message!2222"


@pytest.fixture(name='rabbit')
def init_queue():
    return RabbitClient()


def test_rmq_client(rabbit):
    status = rabbit.enqueue(routing_key=QUEUES_DETAILS[0]["routing_key"], body=FIRST_MESSAGE)
    assert status is True
    rabbit.basic_consume(
        queue=QUEUES_DETAILS[0]["queue"],
        on_message_callback=first_message_callback,
    )

    status = rabbit.enqueue(routing_key=QUEUES_DETAILS[1]["routing_key"], body=SECOND_MESSAGE)
    assert status is True

    # # rabbit.basic_consume(queue=QUEUES_DETAILS[1]["queue"], on_message_callback=second_message_callback)

    rabbit.close_connection()


# helping functions
def first_message_callback(ct, ch, method, properties, body):  # TODO: check ct and basic cancel
    assert body == FIRST_MESSAGE
    ch.basic_cancel(consumer_tag=ct, nowait=False)


def second_message_callback(ct, ch, method, properties, body): # TODO: check ct and basic cancel
    assert body == SECOND_MESSAGE
    ch.basic_cancel('ct')
