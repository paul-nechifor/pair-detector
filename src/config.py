import os
from os.path import dirname, join

_root_dir = join(dirname(__file__), '..')
_data_dir = join(_root_dir, 'data')


class Config(object):

    def __init__(self, **kwargs):
        # The detected object must be at least this ration of the width/height
        # of the image.
        self.min_image_ratio_x = 0.1
        self.min_image_ratio_y = 0.1
        self.min_image_width = 500
        self.min_image_height = 500
        self.found_dir = join(_data_dir, 'found')
        self.found_crop_dir = join(_data_dir, 'found_crop')
        self.tmp_dir = join(_data_dir, 'tmp')
        self.detector_file = join(_root_dir, 'resources', 'pairs.svm')
        self.subreddit = os.environ.get('subreddits', 'all')

        for key, value in kwargs.items():
            setattr(self, key, value)
