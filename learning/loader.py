import configparser
import os
import numpy as np
import shutil

import RivalsOfAetherSync.roasync.roasync as roasync

# Reference: https://github.com/sorki/python-mnist/blob/master/mnist/loader.py
class ReplayLoader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

    def __load__(self, set_apath):
        '''Load paths to all frame and label data for a given set'''
        xset = []
        xset_apath = os.path.join(set_apath, 'frames')
        xset = [
            os.path.join(xset_apath, xdir_dname)
            for xdir_dname in self.__listdir_subdir_only(xset_apath)
            ]
        yset = []
        yset_apath = os.path.join(set_apath, 'labels')
        yset = [
            os.path.join(yset_apath, ydir_dname)
            for ydir_dname in self.__listdir_subdir_only(yset_apath)
        ]
        return (xset, yset)

    def load_training(self):
        '''Load paths to all frame and label data for the training set'''
        print('Loading training set')
        set_apath = self.config['SETS']['PathToTraining']
        (self.x_train, self.y_train) = self.__load__(set_apath)
        print('Finished loading training set. Size is', len(self.x_train))

    def load_testing(self):
        '''Load paths to all frame and label data for the testing set'''
        print('Loading testing set')
        set_apath = self.config['SETS']['PathToTesting']
        (self.x_test, self.y_test) = self.__load__(set_apath)
        print('Finished loading testing set. Size is', len(self.x_test))

    def __get_sync__(self, xdir_apath, ydir_apath):
        '''Get the synced x and y data for a collection of frames and labels'''
        ydir = self.__listdir_np_only__(ydir_apath)
        y_fname = ydir[0]
        y_apath = os.path.join(ydir_apath, y_fname)
        synced = roasync.SyncedReplay()
        synced.create_sync_from_npys(xdir_apath, y_apath)
        x = []
        y = []
        for pair in synced.synced_frames:
            frame = pair.frame
            label = pair.actions
            if label is None:
                label = np.zeros(26)
            else:
                label = np.array(label)
            x.append(frame) # shape: (135, 240, 3)
            y.append(label) # shape: (26,)
        x = np.array(x)
        y = np.array(y)
        return (x, y)

    def __next_batch__(self, x_set, y_set, n=100):
        size = min(n, len(self.y_train))
        batch_x = []
        batch_y = []
        for i in range(n):
            xdir_apath = x_set.pop()
            ydir_apath = y_set.pop()
            (x,y) = self.__get_sync__(xdir_apath, ydir_apath)
            batch_x.append(x)
            batch_y.append(y)
        return (batch_x,batch_y)

    def next_training_batch(self, n=100):
        '''Load a batch of synced x and y data from the training set'''
        return self.__next_batch__(self.x_train, self.y_train, n=n)

    def next_testing_batch(self, n=100):
        '''Load a batch of synced x and y data from the testing set'''
        return self.__next_batch__(self.x_test, self.y_test, n=n)

    def __listdir_subdir_only(self, apath):
        '''listdir filtered to only get folders'''
        return [
            dirent for dirent in os.listdir(apath)
            if os.path.isdir(os.path.join(apath, dirent))
        ]

    def __listdir_np_only__(self, apath):
        '''listdir filtered to only get numpy pickles'''
        return [
            dirent for dirent in os.listdir(apath)
            if os.path.isfile(os.path.join(apath, dirent))
            and (dirent.endswith('np') or dirent.endswith('npy'))
            ]
