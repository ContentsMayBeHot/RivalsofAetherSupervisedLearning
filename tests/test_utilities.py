from test_common import learning
from learning import utilities as utls

import numpy as np
import pytest

@pytest.fixture
def next_batch_4800():
    x = np.ones((4800, 135, 240, 1), dtype=int)
    y = np.ones((4800, 9), dtype=int)
    return x, y

@pytest.fixture
def next_clip_95():
    x = np.ones((95, 135, 240, 1), dtype=int)
    y = np.ones((95, 9), dtype=int)
    return x, y

@pytest.fixture
def next_clip_100():
    x = np.ones((100, 135, 240, 1), dtype=int)
    y = np.ones((100, 9), dtype=int)
    return x, y

@pytest.fixture
def next_frame_rgb():
    return np.ones((135, 240, 3), dtype=int)

@pytest.fixture
def next_frame_gray():
    return np.ones((135, 240, 1), dtype=int)

def test_rgb2gray(next_frame_rgb):
    assert utls.rgb2gray(next_frame_rgb).shape == (135, 240, 1)

def test_downscale_img(next_frame_gray):
    pytest.fail('Not implemented')

def generate_clips(next_batch_4800):
    pytest.fail('Not implemented')

def test_pad_clip(next_clip_95):
    x, y = next_clip_95
    x_pad, y_pad = utls.pad_clip(x, (100, 135, 240, 1), y, (100, 9))
    assert x_pad.shape == (100, 135, 240, 1)
    assert y_pad.shape == (100, 9)
    assert 0 not in x_pad[:94]
    assert 0 not in y_pad[:94]
    assert 1 not in x_pad[94:]
    assert 1 not in y_pad[94:]

def test_pad_clip_no_padding_needed(next_clip_100):
    x, y = next_clip_100
    x_pad, y_pad = utls.pad_clip(x, (100, 135, 240, 1), y, (100, 9))
    assert x_pad.shape == (100, 135, 240, 1)
    assert y_pad.shape == (100, 9)
    assert 0 not in x_pad
    assert 0 not in y_pad

def test_reduce_classes():
    pytest.fail('Not implemented')

def test_listdir_subdir_only():
    pytest.fail('Not implemented')

def test_listdir_np_only():
    pytest.fail('Not implemented')