# !/usr/bin/env

import time

from utils.utils import get_logger
from db_handler_mock import get_latest_completed_for_every_context, get_waiting_messages_by_order, change_message_status

LOGGER_PATH = r'C:\Users\Shani Hochma\PycharmProjects\ShaniIsWorking\logs\spreading_handler.logger'
LOGGER_NAME = 'spreading_handler.logger'
logger = get_logger(LOGGER_NAME, LOGGER_PATH)

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


def send_message(m):
    sending_status = WIP
    logger.info("changing status to 'Sending' in db for message: '%s'", m["message_id"])
    change_result = change_message_status(m["message_id"], "Sending")
    if change_result:
        routing_key = m["destination"]
        logger.info("enqueue message: %s to RabbitMQ with routing key '%s'", m["message_id"], m["destination"])
        # TODO: send message to RabbitMQ by message destination


# this message called in case of message enqueue success.
# it changes status in db from 'Sending' to 'Completed'
def on_ack(m):
    msg_id = m["message_id"]
    logger.info("message with id: %s was enqueued successfully", msg_id)
    logger.info("changing status for message id '%s' to 'Completed'", msg_id)
    change_message_status(msg_id, "Completed")
    sending_status = READY


# this message called in case of message enqueue failure.
def on_nack(m):
    change_message_status(m["message_id"], "Waiting") # TODO: check it's 100% that the message didn't enqueue
    logger.error("can't enqueue message with id: '%s'", m["message_id"])
    sending_status = FAILURE


if __name__ == "__main__":

    last_completed_for_every_context = get_latest_completed_for_every_context()
    messages = get_waiting_messages_by_order()

    messages_length = len(messages)
    index = 0

    while index < messages_length:
        ready_to_send = is_ready_to_send(last_completed_for_every_context, messages, index)
        if ready_to_send:
            logger.info("message with id: '%s' is ready to be sent", messages[index]["message_id"])
            send_message(messages[index])
            while sending_status == WIP:    # waiting for enqueue result
                time.sleep(0.1)
            if sending_status == FAILURE:
                logger.error(
                    "failed enqueue message with id: '%s', skipping all messages with same context",
                    messages[index]["message_id"]
                )
                index = get_first_index_of_next_context(messages, index)
                sending_status = READY
        else:
            logger.warning(
                "message with id: '%s' can't be sent yet. waiting to it's prev message id: '%s'",
                messages[index]["message_id"],
                messages[index]["prev_message_id"]
            )
            index = get_first_index_of_next_context(messages, index)
