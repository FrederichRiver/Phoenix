#!/usr/bin/python3

# monitor system info
# cpu, memory, disk, network

import psutil
from typing import Tuple

class SystemInfo(object):
    # init
    def __init__(self):
        self.cpu = 0.0
        self.memory = 0.0
        self.period = 0.0
    
    def _query_mem_usage(self):
        mem = psutil.virtual_memory()
        self.memory = mem.percent
        return self.memory
    
    def _query_cpu_usage(self):
        self.cpu = psutil.cpu_percent(1)
        return self.cpu
    
    def _query_disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent
    
    def _query_net_usage(self) -> Tuple:
        net = psutil.net_io_counters()
        return net.bytes_sent, net.bytes_recv
    
    def mem_usage_warning(self, threshold: int = 85) -> bool:
        self._query_mem_usage()
        if self.memory > 85:
            return True
        else:
            return False
    
    def cpu_usage_warning(self, threshold: int = 85) -> bool:
        self._query_cpu_usage()
        if self.cpu > 85:
            return True
        else:
            return False
    
    def disk_usage_warning(self, threshold: int = 85) -> bool:
        disk_usage = self._query_disk_usage()
        if disk_usage > 85:
            return True
        else:
            return False
        
    def system_report(self) -> str:
        # Report system infomation.
        mem = self._query_mem_usage()
        disk = self._query_disk_usage()
        MB = 1024*1024
        GB = 1024*MB
        sys_info = (
            f"<CPU>: {psutil.cpu_count()}\n"
            f"<Total Memory>: {round(mem.total/MB, 2)}MB\n"
            f"<Total Disk>: {round(disk.total/GB, 2)}GB")
        return sys_info