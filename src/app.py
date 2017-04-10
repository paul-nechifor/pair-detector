import os
from os.path import dirname, join, exists
from uuid import uuid4

import dlib
import praw
import requests
from PIL import Image
from skimage import io

root = join(dirname(__file__), '..')
data_dir = join(root, 'data')
found_dir = join(data_dir, 'found')
found_crop_dir = join(data_dir, 'found_crop')
tmp_dir = join(data_dir, 'tmp')
detector_file = join(root, 'resources', 'pairs.svm')


def main():
    make_dirs(found_dir, found_crop_dir, tmp_dir)
    App().start()


class App(object):

    def __init__(self):
        self.reddit = praw.Reddit()
        self.detector = dlib.simple_object_detector(detector_file)

    def start(self):
        for s in self.get_nsfw_submissions():
            self.handle_submission(s)

    def get_nsfw_submissions(self):
        # subreddit = self.reddit.subreddit(os.environ['subreddits'])
        subreddit = self.reddit.subreddit('all')
        for s in subreddit.stream.submissions():
            if (
                s.over_18 and
                getattr(s, 'preview', None) and
                s.preview.get('images')
            ):
                yield s

    def handle_submission(self, s):
        # TODO: Check that it's big enough.
        uuid = str(uuid4())
        tmp_path = join(tmp_dir, uuid)
        url = s.preview['images'][0]['source']['url']

        with open(tmp_path, 'wb') as f:
            f.write(requests.get(url).content)

        result = self.handle_image(tmp_path)
        if not result:
            os.unlink(tmp_path)
            return
        img, dets = result

        print('Number of targets detected: {}'.format(len(dets)))

        for k, d in enumerate(dets):
            box = [d.left(), d.top(), d.right(), d.bottom()]
            crop_path = join(found_crop_dir, '%s-%s' % (uuid, k))
            img.crop(box).save(crop_path, 'JPEG')

        os.rename(tmp_path, join(found_dir, uuid))

    def handle_image(self, file):
        try:
            dets = self.detector(io.imread(file))
        except (RuntimeError, ValueError, IOError):
            return

        if not dets:
            return

        img = Image.open(file)
        img_size = (img.size[0] + img.size[1]) / 2.0

        dets = [d for d in dets if (d.right() - d.left()) / img_size > 0.18]

        if not dets:
            return

        return img, dets


def make_dirs(*dirs):
    for dir in dirs:
        if not exists(dir):
            os.mkdir(dir)


if __name__ == '__main__':
    main()
