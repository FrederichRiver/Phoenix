#!/usr/bin/python3

# config file reading and writing
# config files are json format
# read_url is open to use


import json
import os

# convert json to dict
# input_file: json file
# output_file: dict object
def json_to_dict(input_file) -> dict:
    # confirm whether the input file exists
    if not os.path.exists(input_file):
        print(f'Error: {input_file} does not exist')
        return None
    with open(input_file, 'r') as f:
        result = f.read()
        j = json.loads(result)
    return j

# function name: read_url
# format like key: url
# key: key in str type
# input_file: json file
# output: url in str type
def read_url(key, input_file) -> str:
    """
    It is a method base on read_json, returns a url.
    """
    _, url = json_to_dict(key, input_file)
    return url


    
