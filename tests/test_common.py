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


class TestImports:
    def test_module(self):
        assert 'learning' in sys.modules

    def test_sync(self):
        from learning import sync

    def test_loader(self):
        from learning import loader

    def test_utilities(self):
        from learning import utilities

class TestSamples:
    def test_replays_exist(self):
        try:
            replays = [
                dirent for dirent in os.listdir(SAMPLE_REPLAYS_PATH)
                if dirent.endswith('.roa')
            ]
            assert len(replays) == 12
        except:
            pytest.fail('Failed to list contents of samples/sample_replays/')

    def test_frames_exist(self):
        xset_path = os.path.join(SAMPLE_SET_PATH, 'frames')
        try:
            xset = os.listdir(xset_path)
            assert len(xset) == 12
        except:
            pytest.fail('Failed to list contents of samples/sample_set/frames')

    def test_labels_exist(self):
        yset_path = os.path.join(SAMPLE_SET_PATH, 'labels')
        try:
            yset = os.listdir(yset_path)
            assert len(yset) == 12
        except:
            pytest.fail('Failed to list contents of samples/sample_set/labels')