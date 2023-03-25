#!/usr/bin/python3

"""
License: MIT
Author:  @phoenix   
Date:    2023-03-25
Purpose: Run a python script as a daemon
Usage:   python3 run.py
"""

import os
import sys
import atexit
import signal

PID_FILE = '/tmp/daemon.pid'
LOG_FILE = '/tmp/daemon.log'

def run(pid_file: str, log_file: str):
    """Run the daemon process"""
    # Check for a pid file to see if the daemon already runs
    if os.path.isfile(pid_file):
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
    # Register a function to handle termination signals
    signal.signal(signal.SIGTERM, sigterm_handler)

    def sigterm_handler(signo, frame):
        raise SystemExit(1)

# Run the main loop
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} start|stop")
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        run(PID_FILE, LOG_FILE)
    elif sys.argv[1] == 'stop':
        if os.path.isfile(PID_FILE):
            with open(PID_FILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print(f"Not running ({PID_FILE})")
            raise SystemExit(1)