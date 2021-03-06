import enum
import os
import multiprocessing as mp
import numpy as np
import random
import shutil
import signal
import sys

import sync
import utilities as utls


def enqueue_samples(queue, x_set, y_set):
    '''Subprocess task for loading and unpacking samples in the background'''
    # Loop until there are no replays left in the set
    while len(x_set) > 0:
        xdir_apath = x_set.pop()
        ydir_apath = y_set.pop()
        if not xdir_apath or not ydir_apath:
            break
        # For each player, unpack a sample and enqueue it
        for y_fname in utls.listdir_np_only(ydir_apath):
            y_apath = os.path.join(ydir_apath, y_fname)
            sample = unpack_sample(xdir_apath, y_apath)
            queue.put(sample, block=True)
    queue.put(None, block=True)
    queue.close()


def unpack_sample(xdir_apath, y_apath):
    '''Get the synced x and y data for a collection of frames and labels'''
    xysync = sync.SyncedReplay()
    xysync.create_sync_from_npys(xdir_apath, y_apath)
    x = []
    y = []
    # For each synced frame in the replay
    for pair in xysync.synced_frames:
        actions = pair.actions
        frame = pair.frame
        frame = utls.rgb2gray(frame)
        frame = utls.downscale_img(frame)
        x.append(frame)
        y.append(utls.reduce_classes(actions))
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
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        print('CTRL+C detected')
        self.kill_training_subprocess()
        self.kill_testing_subprocess()
        print('Successfully killed worker processes')
        sys.exit(1)

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
        set_size = 0
        for ydir_apath in yset:
            set_size += len(utls.listdir_np_only(ydir_apath))
        return xset, yset, set_size

    def load_training_set(self, set_apath, max_queue_size=10):
        '''Load paths to all frame and label data for the training set'''
        self.x_train, self.y_train, set_size = self.__load_set__(set_apath)
        self.train_queue = mp.Queue(maxsize=max_queue_size)
        self.train_subprocess = mp.Process(
                target=enqueue_samples,
                args=(self.train_queue, self.x_train, self.y_train))  # noqa
        self.train_subprocess.start()
        return set_size

    def load_testing_set(self, set_apath, max_queue_size=10):
        '''Load paths to all frame and label data for the testing set'''
        self.x_test, self.y_test, set_size = self.__load_set__(set_apath)
        self.test_queue = mp.Queue(maxsize=max_queue_size)
        self.test_subprocess = mp.Process(
                target=enqueue_samples,
                args=(self.test_queue, self.x_test, self.y_test))  # noqa
        self.test_subprocess.start()
        return set_size

    def next_training_batch(self):
        '''Load a batch of synced x and y data from the training set'''
        return self.train_queue.get(block=True)

    def next_testing_batch(self):
        '''Load a batch of synced x and y data from the testing set'''
        return self.test_queue.get(block=True)

    def __kill_subprocess__(self, sub):
        if sub is not None and isinstance(sub, mp.Process) and sub.is_alive():
            sub.terminate()
            sub = None

    def kill_training_subprocess(self):
        self.__kill_subprocess__(self.train_subprocess)

    def kill_testing_subprocess(self):
        self.__kill_subprocess__(self.test_subprocess)

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
