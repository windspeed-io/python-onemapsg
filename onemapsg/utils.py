# -*- coding: utf-8 -*-

"""
onemapsg.utils
~~~~~~~~~~~~~~

This module contains utilities shared across the package.
"""

from typing import Any, Callable, List, Optional, Type, Union
from urllib.parse import urlencode

import requests
from requests import Response as RequestsResponse

from .api import API
from .response import GeocodeInfo, Response, RouteResult, SearchResult

SAFE_METHODS: List[str] = ["get", "options"]


def to_dict(obj: Any) -> dict:
    """Converts class instances to dictionaries.
    Handles nested objects as well."""
    if not hasattr(obj, "__dict__"):
        return obj
    result: dict = {}
    for key, val in obj.__dict__.items():
        element: Union[List[Union[dict, List[dict]]], dict] = []
        if not key.startswith("__"):
            if isinstance(val, list) and isinstance(element, list):
                for item in val:
                    element.append(to_dict(item))
            else:
                element = to_dict(val)
        result[key] = element
    return result


def make_request(
    endpoint: str, method: str = "get", data: Optional[dict] = None, timeout: int = 15
) -> Response:
    """Makes a request to the given endpoint and maps the response
    to a Response class"""
    method = method.lower()
    request_method: Callable = getattr(requests, method)
    if method not in SAFE_METHODS and data is None:
        raise ValueError("Data must be provided for POST, PUT and PATCH requests.")

    r: RequestsResponse
    if method not in SAFE_METHODS:
        r = request_method(endpoint, json=data, timeout=timeout)
    else:
        r = request_method(endpoint, timeout=timeout)
    return Response(status_code=r.status_code, data=r.json())


def construct_search_query(
    search_val: str, return_geometry: str, get_address_details: str, page_number: int
) -> str:
    """Constructs search query URL compliant with OneMap's requirements."""
    search_params: dict = {
        "searchVal": search_val,
        "returnGeom": "Y" if return_geometry else "N",
        "getAddrDetails": "Y" if get_address_details else "N",
        "pageNum": page_number if page_number else 1,
    }
    search_params_str: str = urlencode(search_params)
    search_url: str = f"{API.search}?{search_params_str}"
    return search_url


def get_search_class() -> Type[SearchResult]:
    """Returns SearchResult class."""
    return SearchResult


def validate_address_type(address_type: str) -> str:
    if address_type.lower() not in ["all", "hdb"]:
        raise ValueError("Invalid `addressType` value - can only be `HDB` or `All`")
    return address_type.lower()


def construct_reverse_geocode_svy21_query(
    location: str,
    token: str,
    buffer: int = 10,
    address_type: str = "all",
    other_features: bool = False,
) -> str:
    """Constructs Reverse Geocode (SVY21) query URL compliant with
    OneMap's requirements."""
    search_params: dict = {
        "location": ",".join([str(loc).strip() for loc in location]),
        "token": token,
        "buffer": buffer,
        "addressType": validate_address_type(address_type),
        "otherFeatures": "Y" if other_features else "N",
    }
    search_params_str: str = urlencode(search_params, safe=",:-")
    search_url: str = f"{API.reverse_geocode}?{search_params_str}"
    return search_url


def get_reverse_geocode_svy21_class() -> Type[GeocodeInfo]:
    """Returns GeocodeInfo class."""
    return GeocodeInfo


construct_reverse_geocode_wgs84_query: Callable = construct_reverse_geocode_svy21_query
get_reverse_geocode_wgs84_class: Callable = get_reverse_geocode_svy21_class


def construct_route_query(
    start: str, end: str, route_type: str, public_transport_options: dict, token: str
) -> str:
    """Constructs route query URL compliant with OneMap's requirements."""
    route_params: dict = {"start": start, "end": end, "routeType": route_type}
    if route_type == "pt" and public_transport_options:
        route_params.update(public_transport_options)
    route_params_str: str = urlencode(route_params, safe=",:-")
    route_url: str = f"{API.route}?{route_params_str}&token={token}"
    return route_url


def get_route_class() -> Type[RouteResult]:
    """Returns RouteResult class."""
    return RouteResult


def coerce_response(cls: Type[Any], data: dict) -> Any:
    """Creates a class object out of given response data and class."""
    return cls(**data)
