# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch

import pytest

from onemapsg import status
from onemapsg.response import Response
from onemapsg.utils import (construct_route_query, construct_search_query,
                            make_request)


@patch('requests.get')
def test_make_get_request(mock_get):
    """Should return Response instance."""
    mock_json = MagicMock()
    mock_json.return_value = {'detail': 'some data'}
    mock_get.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        json=mock_json
    )
    response = make_request('https://testendpoint.com/api/test')
    assert isinstance(response, Response)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'detail': 'some data'}


@patch('requests.post')
def test_make_post_request(mock_post):
    """Should return Response instance."""
    mock_json = MagicMock()
    mock_json.return_value = {'detail': 'some data'}
    mock_post.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        json=mock_json
    )
    response = make_request(
        'https://testendpoint.com/api/test',
        method='post',
        data={'data': 'some data'}
    )
    assert isinstance(response, Response)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'detail': 'some data'}


@patch('requests.post')
def test_make_post_request_without_data(mock_post):
    """Should return ValueError."""
    with pytest.raises(ValueError) as err:
        make_request('https://testendpoint.com/api/test', method='post')
        assert str(err) == str(ValueError(
            'Data must be provided for POST, PUT and PATCH requests.'))


def test_construct_search_query():
    """Should construct correct search query."""
    url = construct_search_query('some address', True, True, 1)
    assert url == ('https://developers.onemap.sg/'
                   'commonapi/search?'
                   'searchVal=some+address&'
                   'returnGeom=Y&'
                   'getAddrDetails=Y&'
                   'pageNum=1')


def test_construct_route_query():
    """Should construct correct route query."""
    url = construct_route_query('1.12,3.21', '1.02,1.05', 'drive',
                                None, 'sometoken')
    assert url == ('https://developers.onemap.sg/'
                   'privateapi/routingsvc/route?'
                   'start=1.12,3.21&'
                   'end=1.02,1.05&'
                   'routeType=drive&'
                   'token=sometoken')
