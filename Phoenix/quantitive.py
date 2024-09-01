#!/usr/bin/python3

# help me to import all the modules I need
import pandas as pd
import datetime
import sys
import uuid
import time


# I design a module named datahub, which can get data from mysql database
# once I send a request to datahub, it will return a dataframe
# q: how to design the interface of datahub?
# a: I design a class named DataHub, and the class has a method named get_data


class DataHub(object):
    def __init__(self, engine):
        # engine is the connection to mysql database
        self.engine = engine
        self.memory = []
        self.FULL_MEM = False
        self.request_queue = []

    # once I run, I will monitor the request
    # if request has been recieved, I will deal with it
    # for a period of time, I will check the memory, make sure the memory is below the limit
    # also I will check the time stamp of the data in memory, make sure the data is below the limit
    def run(self):
        while True:
            # add request into the queue
            # how to add request into the queue?
            # use the method add_request

            if not self.FULL_MEM:
                if self.request_queue:
                    request = self.request_queue.pop()
                    data = self.get_data(request)
                    self.store_data_in_memery(request, data)
            self.check_memory()
            self.check_time()
            time.sleep(1)
    
    # q: how to recieve the request immediately?
    # a: use the method add_request
    # please finish the method add_request
    def add_request(self, request):
        # q: what is the input parameter of add_request?
        # a: the request
        # q: what is the return value of add_request?
        # a: None
        # q: what is the purpose of add_request?
        # a: add the request into the queue
        pass
        # it seems that need communication between threadings?
        # q: how to communicate between threadings?
        # a: use the method put
        # q: what is the method put?
        # a: it is a method of the class Queue
        # q: how to use the method put?
        # a: self.request_queue.put(request)
        # q: what is the purpose of put?
        # a: put the request into the queue
        # q: how to get the request from the queue?
        # a: use the method get
        # q: what is the method get?
        # a: it is a method of the class Queue
        # q: how to use the method get?
        # a: self.request_queue.get()
        # q: what is the purpose of get?
        # a: get the request from the queue
        # q: how to check the queue is empty?
        # a: use the method empty
        # q: what is the method empty?
        # a: it is a method of the class Queue
        # q: how to use the method empty?
        # a: self.request_queue.empty()
        # q: what is the purpose of empty?
        # a: check the queue is empty or not
        # q: how to check the queue is not empty?
        # a: use the method not empty
        # q: what is the method not empty?
        # a: it is a method of the class Queue
        # q: how to use the method not empty?
        # a: self.request_queue.not empty()
        # q: what is the purpose of not empty?
        # a: check the queue is not empty or not
        # q: how to check the queue is full?
        # a: use the method full
        # q: what is the method full?
        # a: it is a method of the class Queue
        # q: how to use the method full?
        # a: self.request_queue.full()
        # q: what is the purpose of full?
        # a: check the queue is full or not





    def get_data(self, request):
        # request is a dictionary, it contains the information of the data
        # q: what information should be included in the request?
        # a: the table name, the start date, the end date, the columns
        # q: how to get the data from mysql database?
        # a: use pandas.read_sql
        # q: how to return the data?
        # a: return a dataframe
        pass

    # I have to resolve the request first, then I use my own library mysql_utils to get the data
    # q: how to resolve the request?
    # a: use the method resolve_request
    # q: what is resolve_request?
    # a: it is a method of the class DataHub
    def resolve_request(self, request):
        # q: what is the return value of resolve_request?
        # a: it is a dictionary, it contains the information of the data
        # q: what information should be included in the return value?
        # a: the table name, the start date, the end date, the columns
        match request["type"]:
            case "stock":
                data = self.engine.get_stock_data(request["table_name"], request["columns"], from = request["start_date"], to = request["end_date"])
        return data
    
    # wrap the data from request
    def wrap_data(self, data):
        w = dict()
        w["data"] = data
        w["id"] = get_unique_id()
        w["ts"] = datetime.datetime.now()
        w["size"] = sys.getsizeof(data)
        return w
    

    # I want to reuse the data that has been requested in past time
    # q: how should I design the memery of datahub?
    # a: I design a dictionary, the key is the request, the value is the dataframe
    # q: how to get the data from the memery?
    # a: use the method get_data_from_memery
    # q: what is get_data_from_memery? it is also a method of the class DataHub?
    # a: yes, it is a method of the class DataHub
    def get_data_from_memery(self, request):
        # q: what is the return value of get_data_from_memery?
        # a: it is a dataframe
        pass

    # q: how to store the data in the memery?
    # a: use the method store_data_in_memery
    # q: what is store_data_in_memery?
    # a: it is a method of the class DataHub
    def store_data_in_memery(self, request, data):
        # q: what is the input parameter of store_data_in_memery?
        # a: the request and the dataframe    
        pass

    # q: how to store data in memory?
    # a: use the dictionary
    # q: I want to set a limit of time for the data in the memery, when the time is over, data will be deleted from memery
    # q: how to set the limit of time?
    # a: use the method set_limit_of_time
    # q: memory is also to be set a limit
    # a: yes, memory is also to be set a limit
    # q: how to set the limit of memory?
    # a: use the method set_limit_of_memory
    # q: how to delete the data from memery?
    # a: use the method delete_data_from_memery
    # q: what is the best way to deal with the limit of time and size? .counter or some other way?
    # a: I think .counter is a good way
    # q: what if when some request for old data, should the counter be updated?
    # a: yes, the counter should be updated
    # q: I want to build a monitor to monitoring the systeme resource. How is my method?
    # a: I think it is a good method
    # q: I want to know whether others have better ideas?
    # a: I think it is a good method
    def set_limit_of_time(self, limit):
        pass

    def set_limit_of_memory(self, limit):
        pass

    def delete_data_from_memery(self, request):
        pass

    # There is no need to build monitor in this module. I have already built it in basic_utils.system_monitor
    # q: I want to know what functions else should I build in this module?
    # a: I think it is enough

# q: how to use the module datahub?
# a: I design a class named DataHub, and the class has a method named get_data

# q: how should I design the dictionary of the data stored in memery?
# a: I design a dictionary, the key is the request, the value is the dataframe
# q: any other values?
# a: I think it is enough
# q: Will memory occupation effect the performance of the system?
# a: yes, it will
# q: how to deal with the problem?
# a: I think it is a good method
# q: I don't think it is a good method
# a: why?
# q: because you say it will effect the performance
# a: yes, it will

# The request should have a unique id, so that the datahub can find the data in memery
# And it should have a time stamp, so that the datahub can delete the data in memery
# I know how to get unique id.

# a function to get unique id
import uuid
def get_unique_id() -> uuid.UUID:
    # q: how to get unique id?
    # a: use uuid.uuid1()
    # show me the code
    return uuid.uuid1()
 
# now the request is a dictionary, the definition is like this
# the request should have a type also. Because I will have different types of request

# request = {
#     'id': get_unique_id(),
#     'table_name': 'table_name',
#     'start_date': 'start_date',
#     'end_date': 'end_date',
#     'columns': 'columns',
#     'time_stamp': 'time_stamp',
#     'type': 'type'
# }

# each time I recive a request, I will resolve the request first

class requestPipeline(Queue):
    def __init__(self, request):
        self.request = request
        self.datahub = DataHub()
        self.data = self.datahub.get_data(self.request)
        self.datahub.store_data_in_memery(self.request, self.data)
# q: Supose I have a data, DataFrame format, with columns ['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
# q: How can I calculate the adj_close?
# a: I think you can use the method of pandas.DataFrame.apply
# q: How to use the method of pandas.DataFrame.apply?
# q: show me the algorithm of calculating adj_close
# a: adj_close = close * adj_factor
# q: How to calculate adj_factor using open, high, low, close, volume and pre_close?
# a: adj_factor = pre_close / close
# q: 使用分红，送股，拆股等数据计算adj_factor的算法具体是什么?




