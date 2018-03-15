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

    def load(self, set_apath):
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
        (self.x_train, self.y_train) = self.load(set_apath)
        print('Finished loading training set. Size is', len(self.x_train))

    def load_testing(self):
        '''Load paths to all frame and label data for the testing set'''
        print('Loading testing set')
        set_apath = self.config['SETS']['PathToTesting']
        (self.x_test, self.y_test) = self.load(set_apath)
        print('Finished loading testing set. Size is', len(self.x_test))

    def get_sync(self, xdir_apath, ydir_apath):
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

    def next_training(self, n=100):
        '''Load a batch of synced x and y data from the training set'''
        size = min(n, len(self.y_train))
        batch_x = []
        batch_y = []
        for i in range(n):
            print('Fetching training batch [{}/{}]'.format(i+1, n))
            xdir_apath = self.x_train.pop()
            ydir_apath = self.y_train.pop()
            (x, y) = self.get_sync(xdir_apath, ydir_apath)
            batch_x.append(x)
            batch_y.append(y)
        return (batch_x, batch_y)

    def next_testing(self, n=100):
        '''Load a batch of synced x and y data from the testing set'''
        size = min(n, len(self.y_test))
        batch_x = []
        batch_y = []
        for i in range(n):
            print('Fetching testing batch [{}/{}]'.format(i+1, n))
            xdir_apath = self.x_test.pop()
            ydir_apath = self.y_test.pop()
            (x, y) = self.get_sync(xdir_apath, ydir_apath)
            batch_x.append(x)
            batch_y.append(y)
        return (batch_x, batch_y)

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
