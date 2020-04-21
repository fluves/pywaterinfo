# -*- coding: utf-8 -*-
"""
The :class:`pywaterinfo.Waterinfo` is the main
class for waterinfo.be data query interactions.
"""

from pkg_resources import DistributionNotFound, get_distribution

from .waterinfo import HIC_BASE, VMM_BASE, Waterinfo

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


__all__ = ["HIC_BASE", "VMM_BASE", "Waterinfo"]
