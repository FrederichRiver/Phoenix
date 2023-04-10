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
from .env_var import LOG_FILE, PROG_NAME
from functools import wraps
import time
import os


# set log file path using logging.config log file is defined in env_var.py by LOG_FILE
LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_TIME_FORMAT)
log = logging.getLogger()
log.addHandler(TimedRotatingFileHandler(LOG_FILE, when='midnight'))


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f"Calling {func.__name__} with {args} and {kwargs}")
        return func(*args, **kwargs)
    return wrapper


# class Log_Monitor
# use this class to monitor the log file
# usage: log_monitor = Log_Monitor()
# log_monitor.run()
# log_monitor.stop()
class Log_Monitor(object):
    # init input is log_file means log file path. default is LOG_FILE in env_var.py
    def __init__(self, log_file: str=LOG_FILE, logger=log):
        self.log_file = log_file
        self.logger = logger
    
    # run function to monitor the log file
    def run(self):
        # checking whether log file is exists every 10s
        while True:
            if os.path.exists(self.log_file):
                # if log file is exists, do nothing
                pass
            else:
                # if log file is not exists, create a new log file，set the wrting mode to 'a' and return the file object to create_file
                create_file = open(self.log_file, 'a')
                # close the file object
                create_file.close()
                # redirect log file onto create_file using dup2
                with open(self.log_file, 'a') as write_null:
                    os.dup2(write_null.fileno(), 1)
                # redirect error file onto create_file using dup2
                with open(self.log_file, 'a') as error_null:
                    os.dup2(error_null.fileno(), 2)
                # write log into log file
                # message content PROG_NAME started with pid
                # PROG_NAME is defined in env_var.py
                # pid is a process id which is defined in file: /tmp/{PROG_NAME}.pid
                # using os.getpid() to get the pid
                self.logger.info(f"{PROG_NAME} started with pid {os.getpid()}.")
            time.sleep(10)