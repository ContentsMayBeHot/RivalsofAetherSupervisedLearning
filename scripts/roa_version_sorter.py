''' roa_version_sorter.py
Author: Matthew James Harrison
Modified: 1/14/2018
Description: Sorts roa files into folders according to game version. Simply
place in the directory with all of your roa files and run!
'''

from os import listdir, path, mkdir, rename
from json import dumps

if __name__ == '__main__':
    for dirent in listdir():
        # Open the next replay file
        if '.roa' not in dirent:
            continue
        fin = open(dirent)
        if fin:
            # Get the version string and then close the file
            ln = fin.readline()
            v = '{}_{}_{}'.format(str(ln[1:3]), str(ln[3:5]), str(ln[5:7]))
            fin.close()
            # Make a directory with the version string as its name
            if not path.exists(v):
                mkdir(v)
            # Move the replay to the new directory
            rename(dirent, path.join(v, dirent))
