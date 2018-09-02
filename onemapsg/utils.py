# -*- coding: utf-8 -*-

"""
onemapsg.utils
~~~~~~~~~~~~~~

This module contains utilities shared across the package.
"""

from urllib.parse import urlencode

import requests

from onemapsg.api import API
from onemapsg.response import Response

SAFE_METHODS = ['get', 'options']


def make_request(endpoint, method='get',
                 data=None):
    """Makes a request to the given endpoint and maps the response
    to a Response class"""
    method = method.lower()
    request_method = getattr(requests, method)
    if method not in SAFE_METHODS and data is None:
        raise ValueError(
            'Data must be provided for POST, PUT and PATCH requests.'
        )
    if method not in SAFE_METHODS:
        r = request_method(endpoint, json=data)
    else:
        r = request_method(endpoint)
    return Response(status_code=r.status_code, data=r.json())


def construct_search_query(search_val, return_geometry,
                           get_address_details, page_number):
    """Constructs search query URL compliant with OneMap's requirements."""
    search_params = {
        'searchVal': search_val,
        'returnGeom': 'Y' if return_geometry else 'N',
        'getAddrDetails': 'Y' if get_address_details else 'N',
        'pageNum': page_number if page_number else 1
    }
    search_params = urlencode(search_params)
    search_url = f'{API.search}?{search_params}'
    return search_url


def construct_route_query(start, end, route_type,
                          public_transport_options, token):
    """Constructs route query URL compliant with OneMap's requirements."""
    route_params = {
        'start': start,
        'end': end,
        'routeType': route_type
    }
    if route_type == 'pt' and public_transport_options:
        route_params.update(public_transport_options)
    route_params = urlencode(route_params, safe=',')
    route_url = f'{API.route}?{route_params}&token={token}'
    return route_url
