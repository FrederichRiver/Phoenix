#!/usr/bin/python3

# a decorator to log function call
# usage: @log_call
# function name log_call
# function input: function
# function output: function
# log file path is defined by LOG_FILE in env_var.py
# log format is like this: [2020-12-01 10:00:00] [INFO]: ["logging content"] defined in log_utils.py

import logging
from logging.handlers import TimedRotatingFileHandler
from .env_var import LOG_FILE, PROG_NAME, LOG_FORMAT, LOG_TIME_FORMAT
from functools import wraps
import time
import os


# set log file path using logging.config log file is defined in env_var.py by LOG_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)
Log = logging.getLogger()
Log.setLevel(logging.INFO)
Time_Handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
Time_Handler.setLevel(logging.INFO)
log_format = logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT)
Time_Handler.setFormatter(log_format)
Log.addHandler(Time_Handler)


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Log.info(f"Calling {func.__name__} with {args} and {kwargs}")
        return func(*args, **kwargs)
    return wrapper

# function log_monitor, parameters: log_file, logger, the same as Log_Monitor
def log_monitor(log_file: str=LOG_FILE, logger=Log):
    while True:
        if os.path.exists(log_file):
            # if log file is exists, do nothing
            time.sleep(10)
        else:
            # if log file is not exists, create a new log file，set the wrting mode to 'a' and return the file object to create_file
            create_file = open(log_file, 'a')
            # close the file object
            create_file.close()
            # redirect log file onto create_file using dup2
            with open(log_file, 'a') as write_null:
                os.dup2(write_null.fileno(), 1)
            # redirect error file onto create_file using dup2
            with open(log_file, 'a') as error_null:
                os.dup2(error_null.fileno(), 2)
            # write log into log file
            # message content PROG_NAME started with pid
            # PROG_NAME is defined in env_var.py
            # pid is a process id which is defined in file: /tmp/{PROG_NAME}.pid
            # using os.getpid() to get the pid
            logger.info(f"{PROG_NAME} started with pid {os.getpid()}.")
