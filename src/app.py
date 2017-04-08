import glob
from os.path import dirname, join, basename

import dlib
from PIL import Image, ImageDraw
from skimage import io

root = join(dirname(__file__), '..')


def handle_image(detector, file):
    try:
        dets = detector(io.imread(file))
    except (RuntimeError, ValueError, IOError):
        return

    if not dets:
        return

    img = Image.open(file)
    img_size = (img.size[0] + img.size[1]) / 2.0
    draw = ImageDraw.Draw(img)
    base = basename(file)

    dets = [d for d in dets if (d.right() - d.left()) / img_size > 0.18]

    if not dets:
        return

    print('Number of targets detected: {}'.format(len(dets)))

    for k, d in enumerate(dets):
        box = [d.left(), d.top(), d.right(), d.bottom()]
        name = '{0}-{2}.{1}'.format(*(base.rsplit('.', 1) + [k]))
        img.crop(box).save(join(root, 'data', 'detected', name), 'JPEG')

    for d in dets:
        box = [d.left(), d.top(), d.right(), d.bottom()]
        draw.rectangle(box, outline=0xFF00FF)

    img.save(join(root, 'data', 'out', base), 'JPEG')


def main():
    detector_file = join(root, 'resources', 'pairs.svm')
    detector = dlib.simple_object_detector(detector_file)
    files = glob.glob(join(root, 'data', 'in', '*.jpg'))
    for file in files:
        handle_image(detector, file)


if __name__ == '__main__':
    main()
