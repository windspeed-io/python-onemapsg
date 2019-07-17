# -*- coding: utf-8 -*-

"""
onemapsg.types
~~~~~~~~~~~~~~

This module contains Type variables.
"""

from typing import Optional, Tuple


class Types:
    GeoPosition = Tuple[Optional[str], Optional[str]]
    TokenPair = Tuple[Optional[str], Optional[int]]
