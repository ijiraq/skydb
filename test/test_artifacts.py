from unittest import TestCase
import os

from astropy.time import Time

from skydb.artifacts import Image
from astropy.io import fits

__PATH__ = os.path.dirname(__file__)
TEST_FITS_FILE = 'data/cutout_1200_2400_1350_2300-1616681p.fits'
TEST_FITS_FILE = os.path.join(__PATH__, TEST_FITS_FILE)

class TestImage(TestCase):
    def setUp(self) -> None:
        self.hdu = fits.open(TEST_FITS_FILE)
        self.image = Image(TEST_FITS_FILE)

    def test__load_keymap(self):
        self.assertEqual(self.image.header[self.image.fits_keyword_map['DATE-OBS']],
                         self.hdu[0].header["DATE-OBS"])

    def test_bounds(self):
        self.assertAlmostEquals(self.image.bounds,
                                (
                                    (213.96726877115992, 213.97527788793573),
                                    (-12.656266526108762, -12.65102587539254),
                                    (Time("2013-04-09 08:43:05.619"), Time("2013-04-09 08:47:52.721"))),
                                5)
