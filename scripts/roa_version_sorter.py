''' roa_version_sorter.py
Author: Matthew James Harrison
Modified: 1/19/2018
Description: Sorts roa files into folders according to game version. Simply
place in the directory with all of your roa files and run!
'''

import os
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('roa.ini')
    if 'RivalsofAether' not in config.sections():
        print('Failed to retrieve path to replays from roa.ini')
        quit()
    fq_replays = config['RivalsofAether']['PathToReplays']

    print('Using path:', fq_replays)
    for dirent in os.listdir(fq_replays):
        # Open the next replay file
        if len(dirent) < 5 or dirent[-4:] != '.roa':
            continue
        fq_dirent = os.path.join(fq_replays, dirent)
        with open(fq_dirent) as fin:
            # Get the version string and then close the file
            ln = fin.readline()
            version = '{}_{}_{}'.format(str(ln[1:3]),
                                        str(ln[3:5]),
                                        str(ln[5:7]))
            fin.close()
            # Make a directory with the version string as its name
            fq_version = os.path.join(fq_replays, version)
            if not os.path.exists(fq_version):
                os.mkdir(fq_version)
            # Move the replay to the new directory
            os.rename(fq_dirent, os.path.join(fq_version, dirent))
