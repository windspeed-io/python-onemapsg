# -*- coding: utf-8 -*-

from onemapsg import status
from onemapsg.response import Response


def test_response():
    """Should construct a Response instance with status_code and data."""
    response = Response(status.HTTP_200_OK, {'detail': 'example response.'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == 'example response.'
