# -*- coding: utf-8 -*-

"""
onemapsg.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains exception classes mapping the exceptions
thrown from the API.
"""


class AuthenticationError(Exception):
    """Raised when client fails to authenticate with the server."""


class BadRequest(Exception):
    """Raised when status 40x is received as a response code."""


class ServerError(Exception):
    """Raised when there are server errors from OneMap SG."""
