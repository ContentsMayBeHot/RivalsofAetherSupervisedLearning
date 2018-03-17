import configparser
import os
import numpy as np
import shutil
import gc

import RivalsOfAetherSync.roasync.roasync as roasync

from keras.utils import Sequence

def load_set(set_apath):
    '''Load paths to all frame and label data for a given set'''
    xset = []
    xset_apath = os.path.join(set_apath, 'frames')
    xset = [
        os.path.join(xset_apath, xdir_dname)
        for xdir_dname in listdir_subdir_only(xset_apath)
        ]
    yset = []
    yset_apath = os.path.join(set_apath, 'labels')
    yset = [
        os.path.join(yset_apath, ydir_dname)
        for ydir_dname in listdir_subdir_only(yset_apath)
    ]
    return (xset, yset)

def unpack_sample(xdir_apath, ydir_apath):
    '''Get the synced x and y data for a collection of frames and labels'''
    ydir = listdir_np_only(ydir_apath)
    y_fname = ydir[0]
    y_apath = os.path.join(ydir_apath, y_fname)
    synced = roasync.SyncedReplay()
    synced.create_sync_from_npys(xdir_apath, y_apath)
    x = []
    y = []
    # For each synced frame in the replay
    for pair in synced.synced_frames:
        frame = pair.frame
        label = pair.actions
        if label is None:
            label = list(np.zeros(26))
        else:
            label = list(label)
        x.append(frame) # shape: (135, 240, 3)
        y.append(label) # shape: (26,)
    return (x, y)

def listdir_subdir_only(apath):
    '''listdir filtered to only get folders'''
    return [
        dirent for dirent in os.listdir(apath)
        if os.path.isdir(os.path.join(apath, dirent))
    ]

def listdir_np_only(apath):
    '''listdir filtered to only get numpy pickles'''
    return [
        dirent for dirent in os.listdir(apath)
        if os.path.isfile(os.path.join(apath, dirent))
        and (dirent.endswith('np') or dirent.endswith('npy'))
        ]

class ROALoader:
    def __init__(self, autoload_training=False, autoload_testing=False):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Initialize sets
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        # Quick load
        if autoload_training:
            self.load_training_set()
        if autoload_testing:
            self.load_testing_set()

    def load_training_set(self):
        '''Load paths to all frame and label data for the training set'''
        set_apath = self.config['SETS']['PathToTraining']
        (self.x_train, self.y_train) = load_set(set_apath)

    def load_testing_set(self):
        '''Load paths to all frame and label data for the testing set'''
        set_apath = self.config['SETS']['PathToTesting']
        (self.x_test, self.y_test) = load_set(set_apath)

    def __next_batch__(self, x_set, y_set, n=1):
        '''Load batch from given sets'''
        batch_x = []
        batch_y = []
        for i in range(n):
            if not x_set or not y_set:
                break
            xdir_apath = x_set.pop()
            ydir_apath = y_set.pop()
            (x,y) = unpack_sample(xdir_apath, ydir_apath)
            batch_x += x
            batch_y += y
        batch_x = np.array(batch_x)
        batch_y = np.array(batch_y)
        gc.collect()
        return (batch_x, batch_y)

    def next_training_batch(self, n=1):
        '''Load a batch of synced x and y data from the training set'''
        return self.__next_batch__(self.x_train, self.y_train, n=n)

    def next_testing_batch(self, n=1):
        '''Load a batch of synced x and y data from the testing set'''
        return self.__next_batch__(self.x_test, self.y_test, n=n)

    def __get_sequence__(self, x_set, y_set, batch_size=1):
        return ROASequence(x_set, y_set, batch_size=batch_size)

    def get_training_sequence(self, batch_size=1):
        return self.__get_sequence__(self.x_train, self.y_train,
                                     batch_size=batch_size)

    def get_testing_sequence(self, batch_size=1):
        return self.__get_sequence__(self.x_test, self.y_test,
                                     batch_size=batch_size)
