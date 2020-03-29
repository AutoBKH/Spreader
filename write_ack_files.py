# !/usr/bin/env python

import uuid
import os
import time

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ACK_PATH = r"C:\Users\Shani Hochma\PycharmProjects\ShaniIsWorking\acks"

ACK_RECORD_PATTERN = """{
    "message_id": "%s",
    "time": "%s"
}
"""


def get_unique_id():
    return str(uuid.uuid4())

# TODO: replace it with real message ids from poller
message_ids = [get_unique_id(), get_unique_id(), get_unique_id(), get_unique_id()]


def write_ack_file(msg_ids):
    unique_file_id = get_unique_id()
    current_time = time.strftime(TIME_FORMAT)
    filename = 'ack_%s.txt' % unique_file_id
    full_filename = os.path.join(ACK_PATH, filename)
    with open(full_filename, 'w') as f:
        for msg_id in msg_ids:
            f.write(ACK_RECORD_PATTERN % (msg_id, current_time))

if __name__ == "__main__":
    write_ack_file(message_ids)

