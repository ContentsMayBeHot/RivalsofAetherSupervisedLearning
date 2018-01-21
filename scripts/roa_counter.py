''' roa_counter.py
Author: Matthew James Harrison
Modified: 1/20/2018
Description: Counts ROA files within a subtree of the file system.
'''

import configparser
import os

def count(path, search, tab=""):
    print('{}Searching for "{}" files in "{}"'.format(tab, search, path))
    c = 0
    dir = os.listdir(path)

    for dirent in dir:
        subpath = os.path.join(path, dirent)
        if os.path.isdir(subpath):
            c += count(subpath, search, tab + '  ')
        elif dirent.endswith(search):
            c += 1
    print('{}Found: {}!'.format(tab, c))
    return c

def main():
    config = configparser.ConfigParser()
    config.read('roa.ini')
    path = config['RivalsofAether']['PathToReplays']
    search = '.roa'
    c = count(path, search)
    print('Final count: {}!'.format(c))

if __name__ == "__main__":
    main()
