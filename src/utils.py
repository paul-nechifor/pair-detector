import os
from os.path import exists

import requests


def make_dirs(*dirs):
    for dir in dirs:
        if not exists(dir):
            os.mkdir(dir)


def download_url(url, path):
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)
