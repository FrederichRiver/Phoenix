#!/usr/bin/python3

"""
License: MIT
Author:  @phoenix   
Date:    2023-03-25
Purpose: Run a python script as a daemon
Usage:   python3 run.py
"""
import atexit
import os
import signal
import sys
import time
from threading import Thread
from basic_utils.log_utils import Log
from basic_utils.env_var import PROG_NAME, LOG_FILE, PID_FILE, MANUAL_FILE, TASK_FILE
from basic_utils.task_utils import task_manager

__version__ = '1.0.3'

# PID_FILE = '/tmp/neutrino.pid'
# LOG_FILE = '/opt/neutrino/log/run.log'
# MANUAL_FILE = '/opt/neutrino/manual'
# PROG_NAME = 'neutrino'

def run(pid_file: str, log_file: str):
    """Run the daemon process"""
    # Check for a pid file to see if the daemon already runs
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            pid = int(f.read())
        try:
            # Check if the pid is still running
            os.kill(pid, 0)
        except OSError:
            # Process is not running
            pass
        else:
            raise RuntimeError(f"Already running ({pid_file})")
    # Start the daemon
    if os.fork() > 0:
        raise SystemExit(0)
    os.chdir('/')
    os.umask(0)
    os.setsid()
    if os.fork() > 0:
        raise SystemExit(0)
    sys.stdout.flush()
    sys.stderr.flush()
    # redirect stdout
    with open(log_file, 'a') as write_null:
        # Redirect to 1 which means stdout
        os.dup2(write_null.fileno(), 1)
    # redirect stderr
    with open(log_file, 'a') as error_null:
        # Redirect to 2 which means stderr
        os.dup2(error_null.fileno(), 2)

    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        # Register an exit function to remove the pid file
        atexit.register(os.remove, pid_file)
    Log.info(f"{PROG_NAME} started with pid {os.getpid()}.")
    # Register a function to handle termination signals
    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)

def logfile_monitor(log_file: str):
    # A parallel programe which monitoring the log file.
    # If log file is not exists, it will create one and
    # relocalize the file.
    while True:
        if os.path.exists(log_file):
            time.sleep(10)
        else:
            create_file = open(log_file, 'a')
            create_file.close()
            with open(log_file, 'a') as write_null:
                os.dup2(write_null.fileno(), 1)
            with open(log_file, 'a') as error_null:
                os.dup2(error_null.fileno(), 2)
            Log.info(f"{PROG_NAME} started with pid {os.getpid()}.")


def task_pipeline(taskfile=None, task_pipeline_name='Default', task_utils=None):
    # init task manager and main
    if not os.path.exists(taskfile):
        raise FileNotFoundError(taskfile)
    task_manager = task_utils
    task_manager.start()
    Log.info(f"{PROG_NAME} started with pid {os.getpid()}.")
    while True:
        # task_manager.task_report()
        # task_manager.task_solver.load_event()
        task_list = task_manager.check_task_list()
        task_manager.task_manage(task_list)
        time.sleep(3600)

def main(pid_file: str, log_file: str, task_file: str, prog_name: str, task_utils=None):
    run(pid_file, log_file)
    LM = Thread(target=logfile_monitor, args=(log_file,), name='neu_lm', daemon=True)
    LM.start()
    # while True:
    #     pass
    task_pipeline(task_file, prog_name, task_utils)
    

# Run the main loop
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} start|stop")
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        main(PID_FILE, LOG_FILE, TASK_FILE, PROG_NAME, task_manager)
    elif sys.argv[1] == 'stop':
        if os.path.isfile(PID_FILE):
            with open(PID_FILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
            Log.info(f"{PROG_NAME} stopped.")
        else:
            print(f"Not running ({PID_FILE})")
            raise SystemExit(1)
    elif sys.argv[1] == 'clear':
        with open(LOG_FILE, 'w') as f:
            pass
    elif sys.argv[1] == 'log':
        os.system(f"cat {LOG_FILE}")
    elif sys.argv[1] == 'version':
        print(__version__)
    elif sys.argv[1] == 'help':
        os.system(f"cat {MANUAL_FILE}")
    else:
        print('Unknown command {!r}'.format(sys.argv[1]))
        raise SystemExit(1)