# -*- coding: utf-8 -*-

"""
onemapsg.response
~~~~~~~~~~~~~~~~~

This module contains the Response class.
"""


class Response:

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data
