#!/usr/bin/python3

# utils for text operation

# function name drop_space
# remove space from a string
# input_str: a string
# return: a string without space
def drop_space(input_str: str) -> str:
    no_space_text = input_str.replace(' ', '')
    return no_space_text
