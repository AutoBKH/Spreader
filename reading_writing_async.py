# !/usr/bin/env
import os
import time

FILE_PATH = "test.bin"
FILENAME = "test.bin"
LIMIT_IN_SECONDS = 5

f1 = open(FILE_PATH, "w")
f2 = open(FILE_PATH, "r")

try:
    os.rename(FILENAME, FILENAME)
except PermissionError:     # in ntfs it will raise an error. in ext4 no error will be raised.
    print("can't rename an open file in NTFS file system")


# using last modified to define if we can start read a file or not
last_modified = os.path.getmtime(FILE_PATH)
now = time.time()
diff_in_seconds = now - last_modified
if diff_in_seconds > LIMIT_IN_SECONDS:
    print("Ready to read file")

