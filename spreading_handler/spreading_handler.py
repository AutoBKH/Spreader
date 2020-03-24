# !/usr/bin/env

import time

from utils.utils import get_logger
from db_handler_mock import get_latest_completed_for_every_context, get_waiting_messages_by_order, change_message_status
from rmq.rmq import RabbitClient

LOGGER_PATH = r'C:\Users\Shani Hochma\PycharmProjects\ShaniIsWorking\logs\spreading_handler.logger'
LOGGER_NAME = 'spreading_handler.logger'
logger = get_logger(LOGGER_NAME)

"""
    * At this implementations, there are some assumptions:
    * 1) every message have at most one dependency
    * 2) If messages x, y are at the same context and submit_time(x) < submit_time(y):
    *       a. x can be a dependency of y but not vise versa
    *       b. x must be sent before y
    * 3) Messages with context == "" means there is no context,
    *       this kinds of messages can always be sent because is has no dependencies
"""

WIP = 0     # means: work in progress (Waiting for enqueue result)
READY = 1
FAILURE = -1

sending_status = READY


def is_ready_to_send(cache, msgs, i):
    dependant_message = msgs[i]["prev_message_id"]
    if dependant_message is None:
        return True
    if i == 0 or msgs[i - 1]["context"] != msgs[i]["context"]:
        last_completed_message = cache[msgs[i]["context"]]
        return dependant_message == last_completed_message["message_id"]
    return dependant_message == msgs[i - 1]["message_id"]


# if no more messages, i == len(msgs) will be returned
def get_first_index_of_next_context(msgs, i):
    if i >= len(msgs):
        return len(msgs)
    current_context = msgs[i]["context"]
    logger.info("skipping all next messages with same context: '%s'", current_context)
    i += 1
    while i < len(msgs) and msgs[i]["context"] != "" and msgs[i]["context"] == current_context:
        i += 1
    return i


def send_message(m, rmq):
    global sending_status
    sending_status = WIP
    message_id = m["message_id"]
    logger.info("changing status to 'Sending' in db for message: '%s'", message_id)
    is_successfully_changed = change_message_status(message_id, "Sending")
    if is_successfully_changed:
        routing_key = m["destination"]
        logger.info(
            "enqueue message with id: '%s' to RabbitMQ with routing key '%s' and body: '%s'",
            message_id,
            routing_key,
            m["body"]
        )

        is_success = rmq.enqueue(routing_key=routing_key, body=m["body"])
        if is_success:
            on_ack(m)
        else:
            on_nack(m)


# this message called in case of message enqueue success.
# it changes status in db from 'Sending' to 'Completed'
def on_ack(m):
    msg_id = m["message_id"]
    logger.info("message with id: %s was enqueued successfully", msg_id)
    logger.info("changing status for message id '%s' to 'Completed'", msg_id)
    change_message_status(msg_id, "Completed")
    global sending_status
    sending_status = READY


# this message called in case of message enqueue failure.
def on_nack(m):
    change_message_status(m["message_id"], "Waiting")   # TODO: check it's 100% that the message didn't enqueue
    logger.error(
        "can't enqueue message with id: '%s', routing_key: '%s', body: '%s'. changing status in db back to 'Waiting'",
        m["message_id"],
        m["routing_key"],
        m["body"]
    )
    global sending_status
    sending_status = FAILURE


def spread_messages(cache, msgs):
    global sending_status
    messages_length = len(messages)
    index = 0

    while index < messages_length:
        ready_to_send = is_ready_to_send(cache, msgs, index)
        if ready_to_send:
            logger.info("message with id: '%s' is ready to be sent", msgs[index]["message_id"])
            send_message(msgs[index], rabbit)
            while sending_status == WIP:  # waiting for enqueue result
                time.sleep(0.1)
            if sending_status == FAILURE:
                logger.error(
                    "failed enqueue message with id: '%s', skipping all messages with same context",
                    msgs[index]["message_id"]
                )
                index = get_first_index_of_next_context(msgs, index)
                sending_status = READY
            else:
                index += 1
        else:
            logger.warning(
                "message with id: '%s' can't be sent yet. waiting to it's prev message id: '%s'",
                msgs[index]["message_id"],
                msgs[index]["prev_message_id"]
            )
            index = get_first_index_of_next_context(msgs, index)


if __name__ == "__main__":
    rabbit = RabbitClient()
    while True:
        last_completed_for_every_context = get_latest_completed_for_every_context()
        messages = get_waiting_messages_by_order()
        spread_messages(last_completed_for_every_context, messages)
