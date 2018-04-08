import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa
import learning  # noqa

def test_module_imported():
    assert 'learning' in sys.modules

def test_import_sync():
    from learning import sync

def test_import_loader():
    from learning import loader

def test_import_utilities():
    from learning import utilities