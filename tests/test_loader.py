import os
import pytest

from test_common import learning, SAMPLE_SET_PATH
from learning import loader

def test_init():
    roa = loader.ROALoader()
    assert roa.x_train == []
    assert roa.y_train == []
    assert roa.x_test == []
    assert roa.y_test == []
    assert roa.train_queue == None
    assert roa.test_queue == None

@pytest.fixture
def loader_with_training_set():
    roa = loader.ROALoader()
    n = roa.load_training_set(SAMPLE_SET_PATH, max_queue_size=12)
    yield n, roa
    roa.train_subprocess.terminate()

def test_load_set(loader_with_training_set):
    n, _ = loader_with_training_set
    assert n is 12

def test_next_batch(loader_with_training_set):
    _, roa = loader_with_training_set
    batch = roa.next_training_batch()
    assert batch is not None
