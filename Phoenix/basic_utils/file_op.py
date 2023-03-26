#!/usr/bin/python3

# pack files into tar.gz
# file name like SH000300_20200501.csv
# select files by date
# tar file of the same date into one tar.gz
# move tar.gz to ftp folder

import os
import re
from typing import List



class StockDataFilePack(object):
    """
    pack files into tar.gz\n
    file name like SH000300_20200501.csv\n
    1 select files by date\n
    2 tar file of the same date into one tar.gz\n
    3 move tar.gz to ftp folder\n
    """
    # use this regex to get date flag
    Rex = re.compile(r'^(\w{2}\d{6}\_)(\d{8})')
    # init input_path and output_path
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.flag_list = []
    
    def get_file_date_flag(self) -> List[str]:
        """
        recognite file name like SH000300_20200501.csv
        generate a list of date flag
        for example: ['20200501', '20200502', '20200503']
        """      
        # list all files in input_path
        file_list = os.listdir(self.input_path)
        temp_file_list = []
        for file in file_list:
            # recognize file date flag
            result = re.match(self.Rex, file)
            if result:
                # get date flag
                temp_file_list.append(result[2])
        # remove duplicate date flag
        self.flag_list = list(set(temp_file_list))
        return self.flag_list
    
    def pack(self, date_flag: str) -> None:
        # list all files in input_path
        file_list = os.listdir(self.input_path)
        # init a list to store files to be packed
        pack_list = []
        file_pattern = re.compile(r"^\w{2}\d{6}\_" + date_flag)
        for file in file_list:
            # if file name match the pattern, add it to pack_list
            if re.match(file_pattern, file):
                pack_list.append(file)
        # if pack_list is not empty, generate a long string of file names
        if pack_list:
            pack_file = ' '.join(pack_list)
            # change dir to input_path
            os.chdir(self.input_path)
            # pack files into tar.gz
            os.system(f"tar -czvf stock_data_{date_flag}.tar.gz {pack_file}")
            # move tar.gz to output_path
            os.system(f"cp stock_data_{date_flag}.tar.gz {self.output_path}")
        # remove files in pack_list
        for data_file in pack_list:
            os.system(f"rm {data_file}")
