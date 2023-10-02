import os
from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time
from astropy import units
from astropy.units import Quantity
import sip_tpv
import yaml

from .config import fits_keyword_map


class Image(object):
    """
    A class to represent an image artifact.
    """

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            The path to the image artifact.
        """
        self.path = path
        self._data = None
        self._header = None
        self._obs_time = None
        self._wcs = None
        self._bounds = None
        self._exptime = None
        self.fits_keyword_map = fits_keyword_map
        fits_keyword_map_file = fits_keyword_map['filename']
        if os.access(fits_keyword_map_file, os.R_OK):
            self.update_keymap(fits_keyword_map_file)

    def update_keymap(self, keymap_file) -> None:
        """
        Update the fits_keyword_map with a new dictionary.
        """
        with open(keymap_file, 'r') as f:
            self.fits_keyword_map.update(yaml.load(f, Loader=yaml.FullLoader))

    @property
    def header(self) -> fits.header.Header:
        """
        The header of the image artifact.
        """
        if self._header is None:
            self._header = fits.getheader(self.path)
            sip_tpv.pv_to_sip(self._header)
        return self._header
    
    @property
    def wcs(self) -> WCS:
        """
        The WCS of the image artifact.
        """
        if self._wcs is None:
            self._wcs = WCS(self.header)
        return self._wcs
    
    @property
    def obs_time(self) -> Time:
        """
        The time of the image artifact.
        """
        if self._obs_time is None:
            DATEOBS = self.header[self.fits_keyword_map['DATE-OBS']]
            UTCOBS = self.header[self.fits_keyword_map['UTC-OBS']]
            self._obs_time = Time(f"{DATEOBS} {UTCOBS}",
                                  format='iso', scale='utc')
        return self._obs_time

    @property
    def exptime(self) -> Quantity:
        """
        The exposure time of the image artifact.
        """
        if self._exptime is None:
            self._exptime = self.header[self.fits_keyword_map['EXPTIME']] * units.second
        return self._exptime

    @property
    def bounds(self) -> ((float, float), (float, float), (Time, Time)):
        """
        The bounding box of the image artifact.
        """
        if self._bounds is None:
            ra_dec = (self.wcs.calc_footprint()).T
            ra = ra_dec[0]
            dec = ra_dec[1]
            self._bounds = ((ra.min(), ra.max()),
                            (dec.min(), dec.max()),
                            (self.obs_time - self.exptime / 2, self.obs_time + self.exptime / 2))
        return self._bounds
