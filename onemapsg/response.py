# -*- coding: utf-8 -*-

"""
onemapsg.response
~~~~~~~~~~~~~~~~~

This module contains the Response class.
"""

from typing import Any, List, Optional, Tuple

import polyline


class Response:
    def __init__(self, status_code: int, data: dict) -> None:
        self.status_code = status_code
        self.data = data


class BaseResource:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k.lower()):
                setattr(self, k.lower(), v)

    def to_dict(self) -> dict:
        from .utils import to_dict

        return to_dict(self)


class SearchResultItem(BaseResource):

    search_value: Optional[str] = None
    blk_no: Optional[str] = None
    road_name: Optional[str] = None
    building: Optional[str] = None
    address: Optional[str] = None
    postal: Optional[str] = None
    coordinates: Any = None
    lat_long: Any = None

    def __init__(self, **kwargs: Any) -> None:
        if "SEARCHVAL" in kwargs:
            self.search_value = kwargs.pop("SEARCHVAL")
        if "X" in kwargs or "Y" in kwargs:
            x: str = kwargs.pop("X")
            y: str = kwargs.pop("Y")
            self.coordinates = (x, y)
        if "LATITUDE" in kwargs or "LONGITUDE" in kwargs:
            latitude: str = kwargs.pop("LATITUDE")
            longitude: str = kwargs.pop("LONGITUDE")
            self.lat_long = (latitude, longitude)
        super().__init__(**kwargs)


class SearchResult(BaseResource):

    found: Optional[int] = None
    total_num_pages: Optional[int] = None
    page_num: Optional[int] = None
    results: Optional[List[SearchResultItem]] = None

    def __init__(self, **kwargs: Any) -> None:
        if "results" in kwargs:
            results: List[dict] = kwargs.pop("results")
            self.results = [SearchResultItem(**result) for result in results]
        self.total_num_pages: int = kwargs.pop("totalNumPages")
        self.page_num: int = kwargs.pop("pageNum")
        super().__init__(**kwargs)


class GeocodeInfoItem(BaseResource):

    building_name: Optional[str] = None
    block: Optional[str] = None
    road: Optional[str] = None
    postal_code: Optional[str] = None
    coordinates: Any = None
    lat_long: Any = None

    def __init__(self, **kwargs: str) -> None:
        self.building_name = kwargs.get("BUILDINGNAME")
        self.block = kwargs.get("BLOCK")
        self.road = kwargs.get("ROAD")
        self.postal_code = kwargs.get("POSTALCODE")
        x: Optional[str] = kwargs.get("XCOORD")
        y: Optional[str] = kwargs.get("YCOORD")
        self.coordinates = (x, y)
        lat: Optional[str] = kwargs.get("LATITUDE")
        long: Optional[str] = kwargs.get("LONGITUDE")
        self.lat_long = (lat, long)
        super().__init__(**kwargs)


class GeocodeInfo(BaseResource):

    results: Optional[List[GeocodeInfoItem]] = None

    def __init__(self, **kwargs: Any) -> None:
        if "GeocodeInfo" in kwargs:
            results: List[dict] = kwargs.pop("GeocodeInfo")
            self.results = [GeocodeInfoItem(**result) for result in results]
        super().__init__(**kwargs)


class RouteResult(BaseResource):

    # for routeType in ['walk', 'drive', 'cycle']
    status_message: Optional[str] = None
    alternative_names: Optional[List[List[str]]] = None
    route_name: Optional[List[str]] = None
    route_geometry: Optional[str] = None
    route_instructions: Optional[List[List[str]]] = None
    alternative_summaries: Optional[List[dict]] = None
    via_points: Optional[List[Tuple[float, float]]] = None
    route_summary: Optional[dict] = None
    found_alternative: Optional[bool] = None
    status: Optional[int] = None
    via_indices: Optional[List[int]] = None
    hint_data: Optional[dict] = None
    alternative_geometries: Optional[List[str]] = None
    alternative_instructions: Optional[List[List[List[str]]]] = None
    alternative_indices: Optional[List[int]] = None

    # for routeType='pt'
    request_parameters: Any = None
    plan: Any = None
    debug_output: Any = None
    elevation_metadata: Any = None

    def __init__(self, **kwargs: Any) -> None:
        self.request_parameters = kwargs.get("requestParameters")
        self.debug_output = kwargs.get("debugOutput")
        self.elevation_metadata = kwargs.get("elevationMetadata")
        super().__init__(**kwargs)

    @property
    def lat_longs(self) -> Optional[List[Tuple[float, float]]]:
        """Decoded from route_geometry."""
        if self.route_geometry:
            return polyline.decode(self.route_geometry)
        return None
