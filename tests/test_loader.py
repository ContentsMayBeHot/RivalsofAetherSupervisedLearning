import os
import pytest

from test_common import learning
from learning import loader

SAMPLES_PATH = os.path.join('..', 'samples')
SAMPLE_SET_PATH = os.path.join(SAMPLES_PATH, 'sample_set')
SAMPLE_SET_SIZE = 10

def test_init():
    roa = loader.ROALoader()
    assert roa.x_train == []
    assert roa.y_train == []
    assert roa.x_test == []
    assert roa.y_test == []
    assert roa.train_queue == None
    assert roa.test_queue == None

def test_load_set():
    roa = loader.ROALoader()
    n = roa.load_training_set(SAMPLE_SET_PATH, max_queue_size=1)
    assert n == SAMPLE_SET_SIZE

def test_next_batch():
    roa = loader.ROALoader()
    roa.load_training_set(SAMPLE_SET_PATH, max_queue_size=1)
    batch = roa.next_training_batch()