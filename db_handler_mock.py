# !/usr/bin/env

from rmq.rmq import QUEUES_DETAILS

WAITING = "waiting"
COMPLETED = "Completed"

mock_data = [
    # no context
    {
        "time": "2020-01-01 01:00.000",
        "message_id": "1",
        "prev_message_id": None,
        "context": "",
        "body": "message 1",
        "status": COMPLETED,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },
    {
        "time": "2020-01-01 02:00.000",
        "message_id": "2",
        "prev_message_id": None,
        "context": "",
        "body": "message 2",
        "status": WAITING,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },
    {
        "time": "2020-01-01 03:00.000",
        "message_id": "3",
        "prev_message_id": None,
        "context": "",
        "body": "message 3",
        "status": WAITING,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },
    {
        "time": "2020-01-01 04:00.000",
        "message_id": "4",
        "prev_message_id": None,
        "context": "",
        "body": "message 4",
        "status": WAITING,
        "destination": QUEUES_DETAILS[0]["routing_key"],
    },

    # contextA
    {
        "time": "2020-01-01 01:00.000",
        "message_id": "5",
        "prev_message_id": None,
        "context": "contextA",
        "body": "message 1, contextA",
        "status": COMPLETED,
        "destination": QUEUES_DETAILS[1]["routing_key"],
    },
    {
        "time": "2020-01-01 02:10.000",
        "message_id": "6",
        "prev_message_id": "5",
        "context": "contextA",
        "body": "message 2, contextA",
        "status": WAITING,
        "destination": QUEUES_DETAILS[1]["routing_key"],
    },
    {
        "time": "2020-01-01 02:50.000",
        "message_id": "7",
        "prev_message_id": "6",
        "context": "contextA",
        "body": "message 3, contextA",
        "status": WAITING,
        "destination": QUEUES_DETAILS[1]["routing_key"],
    },

    # contextB
    {
        "time": "2020-01-01 10:10.000",
        "message_id": "8",
        "prev_message_id": None,
        "context": "contextB",
        "body": "message 1, contextB",
        "status": COMPLETED,
        "destination": QUEUES_DETAILS[2]["routing_key"],
    },
    {
        "time": "2020-01-01 11:00.000",
        "message_id": "10",
        "prev_message_id": "9",
        "context": "contextB",
        "body": "message 3, contextB",
        "status": WAITING,
        "destination": QUEUES_DETAILS[2]["routing_key"],
    },
    {
        "time": "2020-01-01 12:00.000",
        "message_id": "11",
        "prev_message_id": "10",
        "context": "contextB",
        "body": "message 4, contextB",
        "status": WAITING,
        "destination": QUEUES_DETAILS[2]["routing_key"],
    },
]


# latest with status "completed", without messages with context == ""
def get_latest_completed_for_every_context():
    return {
        "contextA": {
            "time": "2020-01-01 01:00.000",
            "message_id": "5",
            "prev_message_id": None,
            "context": "contextA",
            "body": "message 1, contextA",
            "status": COMPLETED,
            "destination": QUEUES_DETAILS[1]["routing_key"],
        },
        "contextB": {
            "time": "2020-01-01 10:10.000",
            "message_id": "8",
            "prev_message_id": None,
            "context": "contextB",
            "body": "message 1, contextB",
            "status": COMPLETED,
            "destination": QUEUES_DETAILS[2]["routing_key"],
        }
    }


#
def get_waiting_messages_by_order():
    return [

        # no context
        {
            "time": "2020-01-01 02:00.000",
            "message_id": "2",
            "prev_message_id": None,
            "context": "",
            "body": "message 2",
            "status": WAITING,
            "destination": QUEUES_DETAILS[0]["routing_key"],
        },
        {
            "time": "2020-01-01 03:00.000",
            "message_id": "3",
            "prev_message_id": None,
            "context": "",
            "body": "message 3",
            "status": WAITING,
            "destination": QUEUES_DETAILS[0]["routing_key"],
        },
        {
            "time": "2020-01-01 04:00.000",
            "message_id": "4",
            "prev_message_id": None,
            "context": "",
            "body": "message 4",
            "status": WAITING,
            "destination": QUEUES_DETAILS[0]["routing_key"],
        },

        # contextA
        {
            "time": "2020-01-01 02:10.000",
            "message_id": "6",
            "prev_message_id": "5",
            "context": "contextA",
            "body": "message 2, contextA",
            "status": WAITING,
            "destination": QUEUES_DETAILS[1]["routing_key"],
        },
        {
            "time": "2020-01-01 02:50.000",
            "message_id": "7",
            "prev_message_id": "6",
            "context": "contextA",
            "body": "message 3, contextA",
            "status": WAITING,
            "destination": QUEUES_DETAILS[1]["routing_key"],
        },

        # contextB
        {
            "time": "2020-01-01 11:00.000",
            "message_id": "10",
            "prev_message_id": "9",
            "context": "contextB",
            "body": "message 3, contextB",
            "status": WAITING,
            "destination": QUEUES_DETAILS[2]["routing_key"],
        },
        {
            "time": "2020-01-01 12:00.000",
            "message_id": "11",
            "prev_message_id": "10",
            "context": "contextB",
            "body": "message 4, contextB",
            "status": WAITING,
            "destination": QUEUES_DETAILS[2]["routing_key"],
        },

        # contextC
        {
            "time": "2020-01-01 11:00.000",
            "message_id": "11",
            "prev_message_id": None,
            "context": "contextC",
            "body": "message 1, contextC",
            "status": WAITING,
            "destination": QUEUES_DETAILS[3]["routing_key"],
        },
        {
            "time": "2020-01-01 12:00.000",
            "message_id": "12",
            "prev_message_id": "11",
            "context": "contextC",
            "body": "message 2, contextC",
            "status": WAITING,
            "destination": QUEUES_DETAILS[3]["routing_key"],
        },
    ]


def change_message_status(message_id, new_status):
    print("message_id: " + message_id, "new_status: " + new_status)
    return True
