import json
import os
from os.path import exists

import requests
import praw


def make_dirs(*dirs):
    for dir in dirs:
        if not exists(dir):
            os.mkdir(dir)


def download_url(url, path):
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)


def write_json(path, data):
    with open(path, 'w') as f:
        f.write(json_dump(data))


def json_dump(data):
    return json.dumps(data, indent=2, sort_keys=True, separators=(',', ': '))


def to_json_data(obj):
    return _to_json_data(set(), obj)


def _to_json_data(seen, obj):
    if id(obj) in seen or isinstance(obj, praw.Reddit):
        return None
    if isinstance(obj, (int, long, float, basestring, bool)):
        return obj
    seen.add(id(obj))

    if isinstance(obj, (list, set, tuple)):
        return [_to_json_data(seen, x) for x in obj]

    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    if isinstance(obj, dict):
        return {k: _to_json_data(seen, v) for k, v in obj.items()}

    return [None, repr(obj), repr(type(obj))]
