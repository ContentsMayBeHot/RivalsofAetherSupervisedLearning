import enum
import os
import multiprocessing as mp
import numpy as np
import shutil
import sys

import sync
import utilities as utls


def enqueue_samples(queue, x_set, y_set):
    '''Subprocess task for loading and unpacking samples in the background'''
    while len(x_set) > 0:
        xdir_apath = x_set.pop()
        ydir_apath = y_set.pop()
        if not xdir_apath or not ydir_apath:
            break
        sample = unpack_sample(xdir_apath, ydir_apath)
        queue.put(sample, block=True)
    queue.put(None, block=True)
    queue.close()


def unpack_sample(xdir_apath, ydir_apath):
    '''Get the synced x and y data for a collection of frames and labels'''
    ydir = utls.listdir_np_only(ydir_apath)
    y_fname = ydir[0]
    y_apath = os.path.join(ydir_apath, y_fname)
    xysync = sync.SyncedReplay()
    xysync.create_sync_from_npys(xdir_apath, y_apath)
    x = []
    y = []
    # For each synced frame in the replay
    for pair in xysync.synced_frames:
        frame = utls.rgb2gray(pair.frame)
        label = utls.reduce_classes(pair.actions)
        x.append(frame)  # shape: (135, 240, 1)
        y.append(label)  # shape: (9,)
    return x, y


class ROALoader:
    def __init__(self):
        # Initialize sets
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.train_queue = None
        self.train_subprocess = None
        self.test_queue = None
        self.test_subprocess = None

    def __load_set__(self, set_path):
        '''Load paths to all frame and label data for a given set'''
        xset = []
        xset_apath = os.path.join(set_path, 'frames')
        xset = [
            os.path.join(xset_apath, xdir_dname)
            for xdir_dname in utls.listdir_subdir_only(xset_apath)
        ]
        yset = []
        yset_apath = os.path.join(set_path, 'labels')
        yset = [
            os.path.join(yset_apath, ydir_dname)
            for ydir_dname in utls.listdir_subdir_only(yset_apath)
        ]
        return xset, yset

    def load_training_set(self, set_apath, max_queue_size=10):
        '''Load paths to all frame and label data for the training set'''
        self.x_train, self.y_train = self.__load_set__(set_apath)
        self.train_queue = mp.Queue(maxsize=max_queue_size)
        self.train_subprocess = mp.Process(
                target=enqueue_samples,
                args=(self.train_queue, self.x_train, self.y_train))  # noqa
        self.train_subprocess.start()
        return len(self.x_train)

    def load_testing_set(self, set_apath, max_queue_size=10):
        '''Load paths to all frame and label data for the testing set'''
        self.x_test, self.y_test = self.__load_set__(set_apath)
        self.test_queue = mp.Queue(maxsize=max_queue_size)
        self.test_subprocess = mp.Process(
                target=enqueue_samples,
                args=(self.test_queue, self.x_test, self.y_test))  # noqa
        self.test_subprocess.start()
        return len(self.x_test)

    def next_training_batch(self):
        '''Load a batch of synced x and y data from the training set'''
        return self.train_queue.get(block=True)

    def next_testing_batch(self):
        '''Load a batch of synced x and y data from the testing set'''
        return self.test_queue.get(block=True)

    def __get_set_count__(self, x_set):
        xsize = 0
        for xdir_apath in x_set:
            if os.path.isdir(xdir_apath):
                xsize += len(os.listdir(xdir_apath))
        return xsize

    def get_training_count(self):
        return self.__get_set_count__(self.x_train)

    def get_testing_count(self):
        return self.__get_set_count__(self.x_test)
