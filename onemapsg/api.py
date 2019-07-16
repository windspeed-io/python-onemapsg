# -*- coding: utf-8 -*-

"""
onemapsg.api
~~~~~~~~~~~~

This module contains the static API endpoints of `OneMap SG`_.

.. _OneMap SG:
https://docs.onemap.sg/
"""

BASE_URL: str = "https://developers.onemap.sg/"

endpoints: dict = dict(
    auth="privateapi/auth/post/getToken",
    search="commonapi/search",
    route="privateapi/routingsvc/route",
    reverse_geocode="privateapi/commonsvc/revgeocodexy",
    reverse_geocode_wgs84="privateapi/commonsvc/revgeocodexy",
    reverse_geocode_svy21="privateapi/commonsvc/revgeocodexy",
)


class APISingleton:
    """
    Maps endpoints into class attributes and prefixes the
    base URL.
    """

    auth: str
    search: str
    route: str
    reverse_geocode: str
    reverse_geocode_svy21: str
    reverse_geocode_wgs84: str

    def __init__(self) -> None:
        for k, v in endpoints.items():
            setattr(self, k, f"{BASE_URL}{v}")


API: APISingleton = APISingleton()
