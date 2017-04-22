from contextlib import contextmanager
from os.path import dirname, join
from shutil import rmtree
from tempfile import mkdtemp

from ..config import Config

_FIXTURE_DIR = join(dirname(__file__), 'fixtures')


@contextmanager
def get_overriden_config(**kwargs):
    data_dir = mkdtemp()
    config = Config(
        found_dir=join(data_dir, 'found'),
        found_crop_dir=join(data_dir, 'found_crop'),
        tmp_dir=join(data_dir, 'tmp'),
    )

    yield config

    rmtree(data_dir)


def get_fixture(path):
    return join(_FIXTURE_DIR, path)
