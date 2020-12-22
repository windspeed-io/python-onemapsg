# -*- coding: utf-8 -*-

"""
onemapsg.client
~~~~~~~~~~~~~~~

This module contains the OneMap SG Client.
"""

import datetime
import inspect
from typing import Any, Callable, Optional

from . import exceptions, status, utils
from .api import API
from .response import GeocodeInfo, Response, RouteResult, SearchResult
from .types import Types
from .utils import coerce_response, make_request


class OneMap:
    """
    Main API Client to interact with OneMap's API.
    """

    _email: Optional[str] = None
    _password: Optional[str] = None
    token: Optional[str] = None
    token_expiry: Optional[int] = None

    def __init__(
        self, email: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        if email is not None and password is not None:
            self._email = email
            self._password = password
            self.token, self.token_expiry = self._connect()

    @property
    def email(self) -> Optional[str]:
        return self._email

    @property
    def password(self) -> Optional[str]:
        return self._password

    def authenticate(self, email: str, password: str) -> None:
        """This can be used after instantiating the client to authenticate,
        if needed. This is mostly to be backwards compatible with the old
        _connect. We'll probably deprecate _connect at some point in favour
        of this."""

        self._email = email
        self._password = password
        self.token, self.token_expiry = self._connect()

    def _connect(self) -> Types.TokenPair:
        """Retrieves token and stores it. Each token is valid
        for 3 days."""
        login_details: dict = dict(email=self.email, password=self.password)
        response: Response = make_request(API.auth, method="post", data=login_details)
        if response.status_code == status.HTTP_200_OK:
            return (
                response.data["access_token"],
                int(response.data["expiry_timestamp"]),
            )
        elif status.is_client_error(response.status_code):
            raise exceptions.AuthenticationError("Failed to authenticate.")
        elif status.is_server_error(response.status_code):
            raise exceptions.ServerError(
                "OneMap SG server error. " "Please try again later."
            )
        return None, None

    def execute(self, action_type: str, *args: Any, **kwargs: Any) -> Optional[Any]:
        # If endpoint is private, then we need to make
        # sure that client credentials are provided.
        endpoint: str = getattr(API, action_type, "")
        if (
            "privateapi" in endpoint
            and self.token is None
            and self.token_expiry is None
        ):
            raise exceptions.AuthenticationError(
                "This call requires authentication, please call authenticate() "
                "with a valid username and password."
            )

        # If token is going to expire within 2 minutes, get a new one
        if (
            "privateapi" in endpoint
            and self.token is not None
            and self.token_expiry is not None
            and self.email is not None
            and self.password is not None
        ):
            current_unix_timestamp: int = int(datetime.datetime.now().strftime("%s"))
            if self.token_expiry - current_unix_timestamp < 120:
                self.authenticate(self.email, self.password)

        callback: Callable = getattr(utils, f"construct_{action_type}_query")
        request_kwargs: dict = dict()
        if "timeout" in kwargs:
            request_kwargs["timeout"] = kwargs.pop("timeout")
        url: str = callback(*args, **kwargs)
        response: Response = make_request(url, **request_kwargs)
        if response.status_code == status.HTTP_200_OK:
            cls_callback: Callable = getattr(utils, f"get_{action_type}_class")
            cls: Any = cls_callback()
            return coerce_response(cls, response.data)
        elif status.is_client_error(response.status_code):
            if "error" in response.data:
                raise exceptions.BadRequest(response.data["error"])
            raise exceptions.BadRequest("Please ensure request is correct.")
        elif status.is_server_error(response.status_code):
            raise exceptions.ServerError(
                "OneMap SG server error. " "Please try again later."
            )

        return None

    def search(
        self,
        search_val: str,
        return_geometry: bool = True,
        get_address_details: bool = True,
        page_number: Optional[int] = None,
        timeout: int = 15,
    ) -> Optional[SearchResult]:
        """
        Returns search results with both latitude, longitude and x, y
        coordinates of the searched location.

        Ref: https://docs.onemap.sg/#search
        """
        name: str = inspect.stack()[0][3]
        search_result: Optional[Any] = self.execute(
            name,
            search_val,
            return_geometry,
            get_address_details,
            page_number,
            timeout=timeout,
        )
        if isinstance(search_result, SearchResult):
            return search_result
        return None

    def route(
        self,
        start: str,
        end: str,
        route_type: str,
        public_transport_options: Optional[str] = None,
        timeout: int = 15,
    ) -> Optional[RouteResult]:
        """
        Returns the distance and returns the drawn path between the specified
        start and end values depending on the route_type.

        Ref: https://docs.onemap.sg/#routing-service
        """
        name: str = inspect.stack()[0][3]
        route_result: Optional[Any] = self.execute(
            name,
            start,
            end,
            route_type,
            public_transport_options,
            self.token,
            timeout=timeout,
        )
        if isinstance(route_result, RouteResult):
            return route_result
        return None

    def reverse_geocode(
        self,
        reverse_type: str,
        location: str,
        buffer: int = 10,
        address_type: str = "all",
        other_features: bool = False,
        timeout: int = 15,
    ) -> Optional[GeocodeInfo]:
        """
        Retrieves a building address that lies within the defined buffer/radius of
        the specified x, y coordinates.

        Road names are returned within 20m of the specified coordinates in JSON format.

        Ref: https://docs.onemap.sg/#reverse-geocode-svy21
        """
        assert reverse_type in [
            "svy21",
            "wgs84",
        ], "`reverse_type` can only be either `svy21` or `wgs84`."
        name: str = inspect.stack()[0][3]
        name = name + f"_{reverse_type}"
        reverse_geocode_result: Optional[Any] = self.execute(
            name,
            location,
            self.token,
            buffer,
            address_type,
            other_features,
            timeout=timeout,
        )
        if isinstance(reverse_geocode_result, GeocodeInfo):
            return reverse_geocode_result
        return None
