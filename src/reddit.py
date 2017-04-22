import os
import shutil
from os.path import join
from uuid import uuid4

import dlib
import praw

from . import image, utils


class RedditHandler(object):

    def __init__(self, config):
        self.config = config
        self.reddit = praw.Reddit()
        self.detector = dlib.simple_object_detector(self.config.detector_file)

    def stream_submissions(self):
        subreddit = self.reddit.subreddit(self.config.subreddit)
        for s in subreddit.stream.submissions():
            if (
                s.over_18 and
                getattr(s, 'preview', None) and
                s.preview.get('images')
            ):
                yield RedditSubmission(self.config, self.detector, s)


class RedditSubmission(object):

    def __init__(self, config, detector, submission):
        self.config = config
        self.detector = detector
        self.submission = submission
        self.uuid = str(uuid4())
        self.tmp_path = None
        self._image = None

    @property
    def url(self):
        return self.submission.preview['images'][0]['source']['url']

    @property
    def image(self):
        if not self._image:
            self._image = image.Image(
                self.config,
                self.detector,
                self.tmp_path,
            )
        return self._image

    def copy_to_found(self):
        new_path = join(self.config.found_dir, self.uuid)
        shutil.copyfile(self.tmp_path, new_path)
        data = {
            'reddit': utils.to_json_data(self.submission),
            'dets': self.image.serializable_dets,
        }
        utils.write_json(new_path + '.json', data)

    def __enter__(self):
        self.tmp_path = join(self.config.tmp_dir, self.uuid)
        utils.download_url(self.url, self.tmp_path)

    def __exit__(self, _type, _value, _traceback):
        os.unlink(self.tmp_path)
