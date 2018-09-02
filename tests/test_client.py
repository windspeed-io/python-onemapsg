# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch

import pytest

from onemapsg import exceptions, status
from onemapsg.client import OneMap


@patch('onemapsg.client.make_request')
def test_client_connect(mock_request):
    """Client should return a OneMap instance with token and
    token_expiry set."""
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={
            'access_token': 'sometoken',
            'expiry_timestamp': '123456'
        }
    )
    onemap = OneMap('email@example.com', 'password')
    assert onemap.token == 'sometoken'
    assert onemap.token_expiry == '123456'


@patch('onemapsg.client.make_request')
def test_client_connect_error_bad_request(mock_request):
    """Any client errors during authentication should return
    AuthenticationError."""
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_400_BAD_REQUEST
    )
    with pytest.raises(exceptions.AuthenticationError) as err:
        OneMap('email@example.com', 'password')
        assert str(err) == 'Failed to authenticate.'


@patch('onemapsg.client.make_request')
def test_client_connect_error_server_error(mock_request):
    """Any server errors during authentication should return ServerError."""
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    with pytest.raises(exceptions.ServerError) as err:
        OneMap('email@example.com', 'password')
        assert str(err) == 'OneMap SG server error. Please try again later.'


@patch('onemapsg.client.OneMap._connect')
@patch('onemapsg.client.make_request')
def test_client_search(mock_request, mock_connect):
    mock_connect.return_value = None, None
    data = {
        'found': 5,
        'totalNumPages': 1,
        'pageNum': 1,
        'results': [
            {
                'SEARCHVAL': 'INLAND REVENUE AUTHORITY OF SINGAPORE (IRAS)',
                'BLK_NO': '55',
                'ROAD_NAME': 'NEWTON ROAD',
                'BUILDING': 'INLAND REVENUE AUTHORITY OF SINGAPORE (IRAS)',
                'ADDRESS': '55 NEWTON ROAD, SINGAPORE 307987',
                'POSTAL': '307987',
                'X': '28983.7537272647',
                'Y': '33554.4361084122',
                'LATITUDE': '1.31972890510723',
                'LONGITUDE': '103.842158118267',
                'LONGTITUDE': '103.842158118267'
            },
            {
                'SEARCHVAL': 'REVENUE HOUSE',
                'BLK_NO': '55',
                'ROAD_NAME': 'NEWTON ROAD',
                'BUILDING': 'REVENUE HOUSE',
                'ADDRESS': '55 NEWTON ROAD, SINGAPORE 307987',
                'POSTAL': '307987',
                'X': '28977.8507137401',
                'Y': '33547.5712691676',
                'LATITUDE': '1.31966682211667',
                'LONGITUDE': '103.842105076401',
                'LONGTITUDE': '103.842105076401'
            }
        ]
    }
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data=data
    )
    search_result = OneMap('email@example.com', 'password').search('307987')
    assert search_result == data


@patch('onemapsg.client.OneMap._connect')
@patch('onemapsg.client.make_request')
def test_client_search_bad_request(mock_request, mock_connect):
    mock_connect.return_value = None, None
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_400_BAD_REQUEST
    )
    with pytest.raises(exceptions.BadRequest) as err:
        OneMap('email@example.com', 'password').search('307987')
        assert str(err) == 'Please ensure request is correct.'


@patch('onemapsg.client.OneMap._connect')
@patch('onemapsg.client.make_request')
def test_client_search_server_error(mock_request, mock_connect):
    mock_connect.return_value = None, None
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    with pytest.raises(exceptions.ServerError) as err:
        OneMap('email@example.com', 'password').search('307987')
        assert str(err) == 'OneMap SG server error. Please try again later.'
