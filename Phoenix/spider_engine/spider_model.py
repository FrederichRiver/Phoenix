import requests
import os
import re
import json
import time
import psutil
from lxml import etree

class SpiderBase(object):
    """
    Basic class
    """
    def __init__(self) -> None:
        self.http_header = {}

    def get(self, url: str):
        """
        Return http response or None.
        """
        response = requests.get(url, headers=self.http_header)
        if response.status_code == 200:
            return response
        else:
            self.fatal_url(url)
            return None

    def fatal_url(self, url: str):
        raise NotImplementedError

    def delay(self, delta: int):
        time.sleep(delta)

# save_bin is a function to save binary data to a file.
# data is the binary data from a http response.
# file_path is the path of the file, type of str.
# file_name is the name of the file, type of str.
# file_type is the type of the file, type of str.
# save_bin first check if the file_path exists, if not, create it.
# save_bin then recieve the data and open a file to write the data. using wb mode.

def save_bin(data, file_path: str, file_name: str, file_type: str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # using os.path.join to join the path and file name into full_name.
    full_name = os.path.join(file_path, f"{file_name}.{file_type}")
    with open(full_name, 'wb') as f:
        f.write(data)

# save_text is a function to save text data to a file.
# all definition is like save_bin.

def save_text(data, file_path: str, file_name: str, file_type: str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # if file_type is None, then full_name is file_path/file_name
    if file_type:
        full_name = os.path.join(file_path, f"{file_name}.{file_type}")
    else:
        full_name = os.path.join(file_path, file_name)
    with open(full_name, 'w') as f:
        f.write(data)
