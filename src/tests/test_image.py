from unittest import TestCase

import dlib

from ..image import Image
from .utils import get_fixture, get_overriden_config


class ImageTestCase(TestCase):

    def test_image_is_detected(self):
        with get_overriden_config() as config:
            config.min_image_ratio_x = 0.01
            config.min_image_ratio_y = 0.01
            config.min_image_width = 100
            config.min_image_height = 100
            detector = dlib.simple_object_detector(config.detector_file)
            image_path = get_fixture('correct.jpg')
            image = Image(config, detector, image_path)
            self.assertEqual(1, len(image.dets))
