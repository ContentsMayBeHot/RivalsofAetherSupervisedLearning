import numpy as np
import os
import pytest

from test_common import SAMPLE_SET_PATH, SAMPLE_SET_X_PATH, SAMPLE_SET_Y_PATH
from test_common import learning
from learning import loader

@pytest.fixture
def loader_train():
    roa = loader.ROALoader()
    n = roa.load_training_set(SAMPLE_SET_PATH, max_queue_size=12)
    yield n, roa
    roa.train_subprocess.terminate()

def test_init():
    roa = loader.ROALoader()
    assert roa.x_train == []
    assert roa.y_train == []
    assert roa.x_test == []
    assert roa.y_test == []
    assert roa.train_queue == None
    assert roa.train_subprocess == None
    assert roa.test_queue == None
    assert roa.test_subprocess == None

def test_load_set(loader_train):
    n, roa = loader_train
    assert n == 12
    assert len(roa.x_train) == 12
    assert len(roa.y_train) == 12

def test_get_count(loader_train):
    _, roa = loader_train
    assert roa.get_training_count() == 8290

def test_unpack_sample():
    name = '2017-10-21-214825120337'
    xdir_path = os.path.join(SAMPLE_SET_X_PATH, name)
    ydir_path = os.path.join(SAMPLE_SET_Y_PATH, name)
    sample = loader.unpack_sample(xdir_path, ydir_path)
    assert isinstance(sample, tuple)
    sample_x, sample_y = sample
    assert len(sample_x) == 535
    assert len(sample_y) == 535
    for x, y in zip(sample_x, sample_y):
        assert x.shape == (135, 240, 1)
        assert y.shape == (9,)

def test_next_batch(loader_train):
    _, roa = loader_train
    for _ in range(12):
        batch = roa.next_training_batch()
        assert batch != None
        assert isinstance(batch, tuple)
        batch_x, batch_y = batch
        assert isinstance(batch_x, list)
        assert isinstance(batch_y, list)
        assert len(batch_x) > 0
        assert len(batch_y) > 0
        for x, y in zip(batch_x, batch_y):
            assert isinstance(x, np.ndarray)
            assert isinstance(y, np.ndarray)
            assert x.shape == (135, 240, 1)
            assert y.shape == (9,)
    batch = roa.next_training_batch()
    assert batch == None
