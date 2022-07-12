#!/usr/bin/python3
import os

PROJ_PATH = '/home/fred/Documents/dev/Phoenix/Phoenix'
# Test
lib_list = ['libbasemodel', 'librestapi']
for lib in lib_list:
    print(f"[Building {lib}]")
    # go into library directory
    os.chdir(f"{PROJ_PATH}/{lib}")
    # run setup script
    os.system("python3 setup.py sdist")
    # remove egg-info file in package
    # os.system(f"rm -r {lib}.egg-info")
    # cp package in lib/dist into root path
    os.system(f"cp -r dist/ {PROJ_PATH}/")
    # remove lib/dist
    os.system("rm -r dist/")
