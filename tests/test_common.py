import numpy as np
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa
import learning  # noqa

SAMPLES_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'samples')
SAMPLE_REPLAYS_PATH = os.path.join(SAMPLES_PATH, 'sample_replays')
SAMPLE_SET_PATH = os.path.join(SAMPLES_PATH, 'sample_set')
SAMPLE_SET_X_PATH = os.path.join(SAMPLE_SET_PATH, 'frames')
SAMPLE_SET_Y_PATH = os.path.join(SAMPLE_SET_PATH, 'labels')


class TestImports:
    def test_module(self):
        assert 'learning' in sys.modules

    def test_sync(self):
        from learning import sync as _

    def test_loader(self):
        from learning import loader as _

    def test_utilities(self):
        from learning import utilities as _

class TestSamples:
    def test_replays_exist(self):
        assert os.path.isdir(SAMPLE_REPLAYS_PATH)
        replays = [
            dirent for dirent in os.listdir(SAMPLE_REPLAYS_PATH)
            if dirent.endswith('.roa')
        ]
        assert len(replays) == 12

    def test_frames_dir(self):
        assert os.path.isdir(SAMPLE_SET_X_PATH)
        xset = os.listdir(SAMPLE_SET_X_PATH)
        assert len(xset) == 12

    def test_labels_dir(self):
        assert os.path.isdir(SAMPLE_SET_Y_PATH)
        yset = os.listdir(SAMPLE_SET_Y_PATH)
        assert len(yset) == 12

    def test_frames(self):
        for xdir in os.listdir(SAMPLE_SET_X_PATH):
            xdir_path = os.path.join(SAMPLE_SET_X_PATH, xdir)
            assert os.path.isdir(xdir_path)
            xdata = [
                dirent for dirent in os.listdir(xdir_path)
                if dirent.endswith('.np') or dirent.endswith('.npy')
            ]
            assert len(xdata) != 0
            for x in xdata:
                xpath = os.path.join(xdir_path, x)
                np.load(xpath)

    def test_labels(self):
        for ydir in os.listdir(SAMPLE_SET_Y_PATH):
            ydir_path = os.path.join(SAMPLE_SET_Y_PATH, ydir)
            assert os.path.isdir(ydir_path)
            ydata = [
                dirent for dirent in os.listdir(ydir_path)
                if dirent.endswith('.np') or dirent.endswith('.npy')
            ]
            assert len(ydata) != 0
            for y in ydata:
                ypath = os.path.join(ydir_path, y)
                np.load(ypath)