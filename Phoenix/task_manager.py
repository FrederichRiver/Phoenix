#!/usr/bin/python3

"""
License: MIT
Author:  @phoenix
Date:    2023-03-25
Purpose: Define a task manager, which can run tasks in certein time\n
"""
import os
import importlib
from redis_engine import redis_engine
from threading import Thread
from datetime import datetime
import time


class task_manager(object):
    # TODO: Define a task manager, which can run tasks in certein time
    def __init__(self) -> None:
        self.task_set = {}
        self.redis_engine = None
        self.module_list = []

    def init_redis(self, host: str, port: int, password: str, db: int=0):
        self.redis_engine = redis_engine(host, port, password, db=db)

    def run(self):
        """
        input a task_name and a task_time, and run the task in the task_time
        """
        count = 0
        while True:
            # sync module
            self.sync_module()
            # run task every 10 seconds
            if count % 10 == 0:
                # query task
                task_list = self.query_task()
                # run task
                self.run_task(task_list)
            count += 1
            time.sleep(1)

    def query_module(self) -> list:
        # query module from redis database
        module_list = self.redis_engine.get_hash('module_name')
        return module_list
    
    # query for sync module
    def query_sync_module(self) -> list:
        current_module_list = self.query_module()
        """
        check the module_name of module in both current_module_list and self.module_list 
        if they are the same, then check their version. 
        if the version of module in current_module_list is newer than  the version of module in self.module_list, 
        then reload the module.
        both module_name and version are both the key of module in dict format.
        """
        module_to_reload = []
        # we use MODULE_NOT_FOUND to check if the module in current_module_list is in self.module_list
        MODULE_NOT_FOUND = 0
        for module in current_module_list:
            MODULE_NOT_FOUND = 1
            for module2 in self.module_list:
                if module['module_name'] == module2['module_name']:
                    if module['version'] > module2['version']:
                        # add module to module_to_reload
                        module_to_reload.append(module)
                        # remove module from module_list
                        self.module_list.remove(module2)
                        MODULE_NOT_FOUND = 0
                        break
            if MODULE_NOT_FOUND:
                module_to_reload.append(module)
        return module_to_reload

    def query_task(self):
        # query task from redis database
        task_list = self.redis_engine.get_hash('task_name')
        return task_list
    
    #  reload module
    def reload_module(self, module: dict):
        # TODO: reload library
        importlib.reload(module['module_name'])

    # sync module
    def sync_module(self):
        # sync module
        module_to_reload = self.query_sync_module()
        # search module in module_list by key module_name
        for module in module_to_reload:
            # reload module
            self.reload_module(module)
            # add module to module_list
            self.module_list.append(module)


    def add_task(self, task_name: str, task_time):
        """
        add a task to the task manager
        """
        pass

    def resolve_task_file(self, task_list_file: str) -> dict:
        """
        resolve the task_list_file, and return a task set
        """
        # check if the task_list_file exists
        if not os.path.isfile(task_list_file):
            raise RuntimeError(f"task_list_file({task_list_file}) not found")
        # read the task_list_file
        with open(task_list_file, 'r') as f:
            task_list = f.readlines()
        # resolve line
        for line in task_list:
            # check if the line is a comment
            if line.startswith('#'):
                continue
            # check if the line is empty
            elif line == '\n':
                continue
            # elif line can be split into two parts by ，
            elif len(line.split(',')) == 2:
                task_name, task_time = line.split(',')
                print(f"task_name: {task_name}, task_time: {task_time}")
                # add task into a task set
                self.task_set[task_name] = task_time
            else:
                raise RuntimeError(f"task_list_file({task_list_file}) format error")
        return self.task_set

    # run task
    def run_task(self, task: dict, args):
        """
        run task in a thread
        """
        th = Thread(target=task, args=args, daemon=True, name=task["task_name"])
        th.start()
        self.task_pool.append(th)
        
    # shutdown task manager
    def __del__(self) -> None:
        # save module_list to redis
        # save task_set to redis
        # shutdown redis
        self.redis_engine.shutdown()
        pass

