import configparser
import enum
import os
import numpy as np
import shutil

import RivalsOfAetherSync.roasync.roasync as roasync

from keras.utils import Sequence

class Actions(enum.Enum):
    LEFT = 0
    LEFT_TAP = 1
    RIGHT = 2
    RIGHT_TAP = 3
    UP = 4
    UP_TAP = 5
    DOWN = 6
    DOWN_TAP = 7
    ATTACK = 8
    SPECIAL = 9
    JUMP = 10
    DODGE = 11
    STRONG = 12
    STRONG_LEFT = 13
    STRONG_RIGHT = 14
    STRONG_UP = 15
    STRONG_DOWN = 16
    ANG_RIGHT = 17
    ANG_UP_RIGHT = 18
    ANG_UP = 19
    ANG_UP_LEFT = 20
    ANG_LEFT = 21
    ANG_DOWN_LEFT = 22
    ANG_DOWN = 23
    ANG_DOWN_RIGHT = 24
    ANG_TOGGLE = 25

class Classes(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    ATTACK = 4
    SPECIAL = 5
    JUMP = 6
    DODGE = 7
    STRONG = 8

def rgb2gray(rgb):
    # https://stackoverflow.com/a/12201744
    # Reduces dimensions from (135, 240, 3) to (135, 240)
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def reduce_classes(y):
    labels = np.zeros(9).tolist()
    if (y[Actions.LEFT.value]
        or y[Actions.LEFT_TAP.value] == 1
        or y[Actions.STRONG_LEFT.value] == 1
        or y[Actions.ANG_UP_LEFT.value] == 1
        or y[Actions.ANG_DOWN_LEFT.value] == 1):
        # Press left
        labels[Classes.LEFT.value] = 1
    if (y[Actions.RIGHT.value] == 1
        or y[Actions.RIGHT_TAP.value] == 1
        or y[Actions.STRONG_RIGHT.value] == 1
        or y[Actions.ANG_UP_RIGHT.value] == 1
        or y[Actions.ANG_DOWN_RIGHT.value] == 1):
        # Press right
        labels[Classes.RIGHT.value] = 1
    if (y[Actions.UP.value]
        or y[Actions.UP_TAP.value] == 1
        or y[Actions.STRONG_UP.value] == 1
        or y[Actions.ANG_UP_RIGHT.value] == 1
        or y[Actions.ANG_UP_LEFT.value] == 1):
        # Press up
        labels[Classes.UP.value] = 1
    if (y[Actions.DOWN.value]
        or y[Actions.DOWN_TAP.value] == 1
        or y[Actions.STRONG_DOWN.value] == 1
        or y[Actions.ANG_DOWN_RIGHT.value] == 1
        or y[Actions.ANG_DOWN_LEFT.value] == 1):
        # Press down
        labels[Classes.DOWN.value] = 1
    if (y[Actions.ATTACK.value] == 1):
        # Press attack
        labels[Classes.ATTACK.value] = 1
    if (y[Actions.SPECIAL.value] == 1):
        # Press special
        labels[Classes.SPECIAL.value] = 1
    if (y[Actions.JUMP.value] == 1):
        # Press jump
        labels[Classes.JUMP.value] = 1
    if (y[Actions.DODGE.value] == 1):
        # Press dodge
        labels[Classes.DODGE.value] = 1
    if (y[Actions.STRONG.value] == 1
        or y[Actions.STRONG_LEFT.value] == 1
        or y[Actions.STRONG_RIGHT.value] == 1
        or y[Actions.STRONG_UP.value] == 1
        or y[Actions.STRONG_DOWN.value] == 1):
        # Press STRONG
        labels[Classes.STRONG.value] = 1
    return np.array(labels)

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
        frame = rgb2gray(pair.frame)
        label = reduce_classes(pair.actions)
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

class ROASequence(Sequence):
    def __init__(self, x_set, y_set, batch_size):
        self.x = x_set
        self.y = y_set
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        x_paths = self.x[idx*self.batch_size : (idx+1)*self.batch_size]
        y_paths = self.y[idx*self.batch_size : (idx+1)*self.batch_size]
        batch_x = []
        batch_y = []
        for xpath,ypath in zip(x_paths, y_paths):
            x, y = unpack_sample(xpath, ypath)
            batch_x += x
            batch_y += y
        return np.array(batch_x), np.array(batch_y)

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
