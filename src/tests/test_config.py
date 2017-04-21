from unittest import TestCase

from .. import config


class ConfigTestCase(TestCase):

    def test_can_set_the_temp_dir(self):
        tmp_dir = '/my/own/TEMP/dir'
        c = config.Config(tmp_dir=tmp_dir)
        self.assertEqual(tmp_dir, c.tmp_dir)
