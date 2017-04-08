import dlib
import glob
from PIL import Image, ImageDraw
from os.path import dirname, join, basename
from skimage import io

root = join(dirname(__file__), '..')
detector_file = join(root, 'resources', 'pairs.svm')

detector = dlib.simple_object_detector(detector_file)

files = glob.glob(join(root, 'data', 'in', '*.jpg'))
out_dir = join(root, 'data', 'out')


for file in files:
    try:
        io_image = io.imread(file)
    except RuntimeError:
        continue
    dets = detector(io_image)
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    if not dets:
        continue
    print('Number of targets detected: {}'.format(len(dets)))
    for k, d in enumerate(dets):
        box = [d.left(), d.top(), d.right(), d.bottom()]
        draw.rectangle(box, outline=0xFF00FF)
    img.save(join(out_dir, basename(file)), 'JPEG')
