# !/usr/bin/env

from db_handler_mock import COMPLETED, WAITING
from rmq.rmq import QUEUES_DETAILS
from spreading_handler.spreading_handler import is_ready_to_send, get_first_index_of_next_context

CACHE = {
    "contextA": {
        "time": "2020-01-01 01:00.000",
        "message_id": "1",
        "prev_message_id": None,
        "context": "contextA",
        "body": "message 1, contextA",
        "status": COMPLETED,
        "destination": QUEUES_DETAILS[1]["routing_key"],
    },
    "contextB": {
        "time": "2020-01-01 10:10.000",
        "message_id": "1",
        "prev_message_id": None,
        "context": "contextB",
        "body": "message 1, contextB",
        "status": COMPLETED,
        "destination": QUEUES_DETAILS[2]["routing_key"],
    }
}

WAITING_MESSAGES = [

    # no context
    {   # 0
        "time": "2020-01-01 02:00.000",
        "message_id": "2",
        "prev_message_id": None,
        "context": "",
        "body": "message 2",
        "status": WAITING,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },
    {  # 1
        "time": "2020-01-01 03:00.000",
        "message_id": "3",
        "prev_message_id": None,
        "context": "",
        "body": "message 3",
        "status": WAITING,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },
    {  # 2
        "time": "2020-01-01 04:00.000",
        "message_id": "4",
        "prev_message_id": None,
        "context": "",
        "body": "message 4",
        "status": WAITING,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },

    # contextA
    {  # 3
        "time": "2020-01-01 02:10.000",
        "message_id": "2",
        "prev_message_id": "1",
        "context": "contextA",
        "body": "message 2, contextA",
        "status": WAITING,
        "destination": QUEUES_DETAILS[1]["routing_key"],
    },
    {  # 4
        "time": "2020-01-01 02:50.000",
        "message_id": "3",
        "prev_message_id": "2",
        "context": "contextA",
        "body": "message 3, contextA",
        "status": WAITING,
        "destination": QUEUES_DETAILS[1]["routing_key"],
    },

    # contextB
    {  # 5
        "time": "2020-01-01 11:00.000",
        "message_id": "3",
        "prev_message_id": "2",
        "context": "contextB",
        "body": "message 3, contextB",
        "status": WAITING,
        "destination": QUEUES_DETAILS[2]["routing_key"],
    },
    {  # 6
        "time": "2020-01-01 12:00.000",
        "message_id": "4",
        "prev_message_id": "3",
        "context": "contextB",
        "body": "message 4, contextB",
        "status": WAITING,
        "destination": QUEUES_DETAILS[2]["routing_key"],
    },
]


def test_is_ready_to_send():
    assert is_ready_to_send(CACHE, WAITING_MESSAGES, 0) == True
    assert is_ready_to_send(CACHE, WAITING_MESSAGES, 1) == True
    assert is_ready_to_send(CACHE, WAITING_MESSAGES, 3) == True
    assert is_ready_to_send(CACHE, WAITING_MESSAGES, 4) == True
    assert is_ready_to_send(CACHE, WAITING_MESSAGES, 5) == False


def test_get_first_index_of_next_context():
    assert get_first_index_of_next_context(WAITING_MESSAGES, 0) == 1
    assert get_first_index_of_next_context(WAITING_MESSAGES, 1) == 2
    assert get_first_index_of_next_context(WAITING_MESSAGES, 3) == 5
    assert get_first_index_of_next_context(WAITING_MESSAGES, 4) == 5
    assert get_first_index_of_next_context(WAITING_MESSAGES, 5) == 7
