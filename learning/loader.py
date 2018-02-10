import os
import shutil

# Reference: https://github.com/sorki/python-mnist/blob/master/mnist/loader.py
class ReplayLoader:
    def __init__(self, dataset_apath='.'):
        self.dataset_apath = dataset_apath
        self.testing_dname = 'testing'
        self.training_dname = 'training'

        self.testing_x = []
        self.testing_y = []

        self.training_x = []
        self.training_y = []

    def load(self, x_apath, y_apath):
        pass

    def load_testing(self):
        return self.testing_x, self.testing_y

    def load_training(self):
        return self.training_x, self.training_y

