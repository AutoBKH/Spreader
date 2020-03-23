# !/usr/bin/env

from db_handler_mock import get_latest_completed_for_every_context, get_waiting_messages_by_order


def is_ready_to_send(cache, msgs, i):
    dependant_message = msgs[i]["prev_message_id"]
    if i == 0:
        last_completed_message = cache[msgs[i]["context"]]
        return dependant_message == last_completed_message["message_id"]
    return dependant_message == msgs[i-1]["message_id"]


def send_message(m):
    # change status to "Sending"
    # send message to queue
    # check sending status
    # if status == success: change status in db to completed
    # can we have a flush message and resend all messages in the same context?
    print(m)
    pass


if __name__ == "__main__":
    last_completed_for_every_context = get_latest_completed_for_every_context()
    messages = get_waiting_messages_by_order()

    messages_length = len(messages)
    index = 0
    while index < messages_length:
        ready_to_send = is_ready_to_send(last_completed_for_every_context, messages, index)
        if ready_to_send:
            send_message(messages[index])
        else:
            current_context = messages[index]["context"]
            while messages[index]["context"] == current_context and index < messages_length:
                index += 1
