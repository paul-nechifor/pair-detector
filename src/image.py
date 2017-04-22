from PIL import Image as PilImage
from skimage import io


class Image(object):

    def __init__(self, config, detector, image_path):
        self.config = config
        self.detector = detector
        self.image_path = image_path
        self._dets = None
        self._image = None

    @property
    def dets(self):
        if not self._dets:
            self._dets = self._get_dets()
        return self._dets

    def _get_dets(self):
        try:
            dets = self.detector(io.imread(self.image_path))
        except (RuntimeError, ValueError, IOError):
            return []

        if not dets:
            return []

        return filter(self._check_det, dets)

    def _check_det(self, det):
        det_width = det.right() - det.left()
        det_height = det.bottom() - det.top()
        image_width, image_height = self.image.size
        return all([
            image_width >= self.config.min_image_width,
            image_height >= self.config.min_image_height,
            float(det_width) / image_width >= self.config.min_image_ratio_x,
            float(det_height) / image_height >= self.config.min_image_ratio_y,
        ])

    @property
    def image(self):
        if not self._image:
            self._image = PilImage.open(self.image_path)
        return self._image
