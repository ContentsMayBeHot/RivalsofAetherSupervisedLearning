import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa
import learning  # noqa


def test_imported():
    assert 'learning' in sys.modules
