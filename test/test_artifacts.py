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
        self.date_obs = fits.getheader(TEST_FITS_FILE)['DATE-OBS']
        self.image = Image(TEST_FITS_FILE)

    def test__load_keymap(self):
        self.assertEqual(self.image.header[self.image.fits_keyword_map['DATE-OBS']], self.date_obs)

    def test_bounds(self):
        self.assertAlmostEqual(self.image.bounds[0][0], 213.96726877115992, places=5)
        self.assertAlmostEqual(self.image.bounds[0][1], 213.97527788793573, places=5)
        self.assertAlmostEqual(self.image.bounds[1][0], -12.656266526108762, places=5)
        self.assertAlmostEqual(self.image.bounds[1][1], -12.65102587539254, places=5)
        self.assertEqual(self.image.bounds[2][0], Time("2013-04-09 08:43:05.619"))
        self.assertEqual(self.image.bounds[2][1], Time("2013-04-09 08:47:52.721"))
