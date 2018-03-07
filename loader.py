import os
import numpy as np
import shutil

# Reference: https://github.com/sorki/python-mnist/blob/master/mnist/loader.py
class ReplayLoader:
    def __init__(self):
        self.dataset_apath = dataset_apath
        self.sets_dname = 'sets'
        self.testing_dname = 'testing'
        self.training_dname = 'training'

        self.testing_frames = []
        self.testing_labels = []

        self.training_frames = []
        self.training_labels = []

    def load(self, frames_apath, labels_apath):
        frames = []
        for dirent in os.listdir(frames_apath):
            dirent_apath = os.path.join(frames_apath, dirent)
            frames.append(np.load(dirent_apath))
        labels = []
        for dirent in os.listdir(labels_apath):
            dirent_apath = os.path.join(frames_apath, dirent)
            labels.append(np.load(dirent_apath))
        return (frames, labels)

    def load_testing(self):
        set_apath = os.path.join(self.sets_dname, self.testing_dname)
        frames_apath = os.path.join(set_apath, 'frames')
        labels_apath = os.path.join(set_apath, 'labels')
        self.testing_frames, self.testing_labels = self.load(frames_apath, labels_apath)

    def load_training(self):
        set_apath = os.path.join(self.sets_dname, self.training_dname)
        frames_apath = os.path.join(set_apath, 'frames')
        labels_apath = os.path.join(set_apath, 'labels')
        self.training_frames, self.training_labels = self.load(frames_apath, labels_apath)
