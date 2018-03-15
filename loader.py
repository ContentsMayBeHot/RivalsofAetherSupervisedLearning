import configparser
import os
import numpy as np
import shutil

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
        print('Loading from', set_apath)

        batch_x = []
        print('Loading frames...')
        xset_apath = os.path.join(set_apath, 'frames')
        for xdir_dname in self.__listdir_subdir_only(xset_apath):
            xdir_apath = os.path.join(xset_apath, xdir_dname)
            for x_fname in self.__listdir_np_only__(xdir_apath):
                x_apath = os.path.join(xdir_apath, x_fname)
                batch_x.append(x_apath)

        batch_y = []
        print('Loading labels...')
        yset_apath = os.path.join(set_apath, 'labels')
        for ydir_dname in self.__listdir_subdir_only(yset_apath):
            ydir_apath = os.path.join(yset_apath, ydir_dname)
            for y_fname in self.__listdir_np_only__(ydir_apath):
                y_apath = os.path.join(ydir_apath, y_fname)
                batch_y.append(y_apath)

        return (batch_x,batch_y)

    def load_training(self):
        set_apath = self.config['SETS']['PathToTraining']
        (self.x_train,self.y_train) = self.load(set_apath)
        return (self.x_train,self.y_train)

    def load_testing(self):
        set_apath = self.config['SETS']['PathToTesting']
        (self.x_test,self.y_test) = self.load(set_apath)
        return (self.x_test,self.y_test)

    def next_training(self, size=100):
        x = []
        y = []
        for i in range(size):
            x.append(np.load(self.x_train.pop()))
            y.append(np.load(self.y_train.pop()))
        return (x,y)

    def next_testing(self, size=100):
        x = []
        y = []
        for i in range(size):
            x.append(np.load(self.x_test.pop()))
            y.append(np.load(self.y_test.pop()))
        return (x,y)

    def __listdir_subdir_only(self, apath):
        return [
            dirent for dirent in os.listdir(apath)
            if os.path.isdir(os.path.join(apath, dirent))
        ]

    def __listdir_np_only__(self, apath):
        return [
            dirent for dirent in os.listdir(apath)
            if os.path.isfile(os.path.join(apath, dirent))
            and (dirent.endswith('np') or dirent.endswith('npy'))
            ]
