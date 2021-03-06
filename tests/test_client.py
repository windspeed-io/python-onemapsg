# -*- coding: utf-8 -*-

import datetime
from unittest.mock import MagicMock, patch

import pytest

from onemapsg import exceptions, response, status
from onemapsg.client import OneMap


def test_client_noauth():
    """Client should instantiate without credentials."""
    onemap = OneMap()
    assert onemap.token is None
    assert onemap.token_expiry is None


@patch("onemapsg.client.make_request")
def test_client_authenticate(mock_request):
    """Client should successfully attach token and toke_expiry
    after instantiation via the `authenticate` method."""
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={"access_token": "sometoken", "expiry_timestamp": "123456"},
    )
    onemap = OneMap()
    onemap.authenticate("email@example.com", "password")
    assert onemap.token == "sometoken"
    assert onemap.token_expiry == 123456


@patch("onemapsg.client.make_request")
def test_client_connect(mock_request):
    """Client should return a OneMap instance with token and
    token_expiry set."""
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={"access_token": "sometoken", "expiry_timestamp": "123456"},
    )
    onemap = OneMap("email@example.com", "password")
    assert onemap.token == "sometoken"
    assert onemap.token_expiry == 123456


@patch("onemapsg.client.make_request")
def test_client_connect_error_bad_request(mock_request):
    """Any client errors during authentication should return
    AuthenticationError."""
    mock_request.return_value = MagicMock(status_code=status.HTTP_400_BAD_REQUEST)
    with pytest.raises(exceptions.AuthenticationError) as err:
        OneMap("email@example.com", "password")
        assert str(err) == "Failed to authenticate."


@patch("onemapsg.client.make_request")
def test_client_connect_error_server_error(mock_request):
    """Any server errors during authentication should return ServerError."""
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    with pytest.raises(exceptions.ServerError) as err:
        OneMap("email@example.com", "password")
        assert str(err) == "OneMap SG server error. Please try again later."


@patch("onemapsg.client.make_request")
def test_client_connect_return_none(mock_request):
    """Token and token_expiry should be None when response from authentication
    endpoint is not 200, 4xx or 5xx"""
    mock_request.return_value = MagicMock(status_code=status.HTTP_301_MOVED_PERMANENTLY)
    onemap = OneMap("email@example.com", "password")
    assert onemap.token is None
    assert onemap.token_expiry is None


def test_client_execute_protected_noauth():
    """Client should raise an error when trying to make a request
    to a protected API when no credentials are provided."""
    with pytest.raises(exceptions.AuthenticationError):
        onemap = OneMap()
        onemap.route("1.23,1.01", "1.01,1.23", "drive")


@patch("onemapsg.client.make_request")
def test_client_execute_return_none(mock_request):
    """Client should return None when an execute() call
    gets a response status that isn't 2xx, 4xx or 5xx"""
    mock_request.return_value = MagicMock(status_code=status.HTTP_301_MOVED_PERMANENTLY)
    onemap = OneMap()
    res = onemap.execute("search", "123456", True, True, None)
    assert res is None


@patch("onemapsg.client.make_request")
def test_client_refresh_token(mock_request):
    """Client should retrieve a new token when making a request
    and existing token is less than 2 minutes from expiring."""
    mock_current_time = int(datetime.datetime.now().strftime("%s"))
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={
            "access_token": "some-token",
            "expiry_timestamp": mock_current_time + 60,  # within 2 minutes
        },
    )
    onemap = OneMap("email@example.com", "password")
    with patch.object(onemap, "authenticate") as mock_authenticate:
        data = {
            "status_message": "Found route between points",
            "alternative_names": [
                ["COMMONWEALTH AVENUE WEST", "NORTH BUONA VISTA ROAD"]
            ],
            "route_name": ["CLEMENTI AVENUE 2", "ULU PANDAN ROAD"],
            "route_geometry": (
                "yr`oAm`k{dEksAstD~e@iW`e@{UxtAqr@pd@sVrOmItC}GZ}GJwDeSmWkm@gb@qKuEyCw"
                "E}AgHJiH\\kE{BaRoCoEsGcLiE{N{AmQvB{QbFkN|E}FzMcPtQmTh|A_iBfCcDzHcKpJa"
                "Mr\\w_@t\\i`@hb@gg@lAkJRqJg@wJeCoMgQ{f@qHsTuC_FiMsT_S_ViVkPkfAyi@oXiN"
                "q{@q_@qn@cU{SsGgEqAiDeAcTsGcd@eMoF{AoBi@uGkB}d@uMwDoA_EsA{QiG_VyJaSkL"
                "kQuN}CgDqJkKqDsFqE_H}CuE}CyEsBsGcDeKuK}f@}FiJ_FaEkKiEgHcAe~@xMsr@`LqM"
                "rB_En@gAy`@kBkVwE{W_^gbAkHg[aFeQaRe^_Nea@iEwYJkYsAyj@KiRkGglAcDqn@KiU"
                "rDkc@nFkY`Lo]lIeQfJgOfcAyhAzJ}KtPsTjIuQxFaQrBcN|E{u@rDgh@hBuYjDy_@zHo"
                "UbI}O|PwSkDuBiP_K{]cTq_Ack@ixAe|@_L}G{LoHynBujAsh@iZiRqK}|@ig@xg@wo@v"
                "{@_gA~q@g}@fUgZp^{`@gDqLv`@oNfTwH~LcIl@gEy@{PqU_V_`@cuAvHwJt^_MvXgMxC"
                "aD"
            ),
            "route_instructions": [
                ["10", "PANDAN LOOP", 853, 0, 89, "853m", "NE", 65, 1, "SW", 245]
            ],
            "alternative_summaries": [
                {
                    "end_point": "REBECCA ROAD",
                    "start_point": "PANDAN LOOP",
                    "total_time": 761,
                    "total_distance": 8133,
                }
            ],
            "via_points": [[1.311549, 103.749657], [1.32036, 103.800156]],
            "route_summary": {
                "end_point": "REBECCA ROAD",
                "start_point": "PANDAN LOOP",
                "total_time": 740,
                "total_distance": 7957,
            },
            "found_alternative": True,
            "status": 200,
            "via_indices": [0, 140],
            "hint_data": {
                "locations": [
                    "NzgBANtqAQBRBQAAAAAAAAQAAAAAAAAAuQIAAEOcAABoAAAAPQMUABcYLwYAAAEB",
                    "0OUAAF4zAQChAwAABAAAAAwAAABIAAAAdQAAACx9AABoAAAAqCUUAFndLwYCAAEB",
                ],
                "checksum": 585417468,
            },
            "alternative_geometries": [
                (
                    "yr`oAm`k{dEksAstD~e@iW`e@{UxtAqr@pd@sVrOmItC}GZ}GJwDeSmWkm@gb@qKu"
                    "EyCwE}AgHJiH\\kE{BaRoCoEsGcLiE{N{AmQvB{QbFkN|E}FzMcPtQmTh|A_iBfCc"
                    "DzHcKpJaMr\\w_@t\\i`@hb@gg@lAkJRqJg@wJeCoMgQ{f@qHsTuC_FiMsT_S_ViV"
                    "kPkfAyi@oXiNq{@q_@qn@cU{SsGgEqAiDeAcTsGcd@eMoF{AoBi@uGkB}d@uMwDoA"
                    "_EsA{QiG_VyJaSkLkQuN}CgDqJkKqDsFqE_H}CuE}CyEsBsGcDeKuK}f@}FiJ_FaE"
                    "kKiEgHcAe~@xMsr@`LqMrB_En@gAy`@kBkVwE{W_^gbAkHg[aFeQaRe^_Nea@iEwY"
                    "JkYsAyj@KiRkGglAcDqn@KiUrDkc@nFkY`Lo]lIeQfJgOfcAyhAzJ}KtPsTjIuQxF"
                    "aQrBcN|E{u@rDgh@hBuYjDy_@zHoUbI}O|PwSkDuBiP_K{]cTq_Ack@ixAe|@_L}G"
                    "{LoHynBujAsh@iZiRqK}|@ig@xg@wo@v{@_gA~q@g}@fUgZp^{`@gDqLv`@oNfTwH"
                    "~LcIl@gEy@{PqU_V_`@cuAvHwJt^_MvXgMxCaD"
                )
            ],
            "alternative_instructions": [
                [
                    ["10", "PANDAN LOOP", 853, 0, 89, "853m", "NE", 65, 1, "SW", 245],
                    ["8", "JALAN BUROH", 217, 9, 23, "217m", "NE", 50, 1, "SW", 230],
                    ["1", "WEST COAST HIGHWAY", 62, 14, 7, "61m", "E", 92, 1, "W", 272],
                ]
            ],
            "alternative_indices": [0, 159],
        }
        mock_request.return_value = MagicMock(status_code=status.HTTP_200_OK, data=data)
        onemap.route("1.23,1.01", "1.01,1.23", "drive")
        mock_authenticate.assert_called_once()


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_client_search(mock_request, mock_connect):
    """Should return SearchResult instance as response."""
    mock_connect.return_value = None, None
    data = {
        "found": 5,
        "totalNumPages": 1,
        "pageNum": 1,
        "results": [
            {
                "SEARCHVAL": "INLAND REVENUE AUTHORITY OF SINGAPORE (IRAS)",
                "BLK_NO": "55",
                "ROAD_NAME": "NEWTON ROAD",
                "BUILDING": "INLAND REVENUE AUTHORITY OF SINGAPORE (IRAS)",
                "ADDRESS": "55 NEWTON ROAD, SINGAPORE 307987",
                "POSTAL": "307987",
                "X": "28983.7537272647",
                "Y": "33554.4361084122",
                "LATITUDE": "1.31972890510723",
                "LONGITUDE": "103.842158118267",
                "LONGTITUDE": "103.842158118267",
            },
            {
                "SEARCHVAL": "REVENUE HOUSE",
                "BLK_NO": "55",
                "ROAD_NAME": "NEWTON ROAD",
                "BUILDING": "REVENUE HOUSE",
                "ADDRESS": "55 NEWTON ROAD, SINGAPORE 307987",
                "POSTAL": "307987",
                "X": "28977.8507137401",
                "Y": "33547.5712691676",
                "LATITUDE": "1.31966682211667",
                "LONGITUDE": "103.842105076401",
                "LONGTITUDE": "103.842105076401",
            },
        ],
    }
    mock_request.return_value = MagicMock(status_code=status.HTTP_200_OK, data=data)
    search_result = OneMap("email@example.com", "password").search("307987")
    assert isinstance(search_result, response.SearchResult)


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_client_search_bad_request(mock_request, mock_connect):
    mock_connect.return_value = None, None
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_400_BAD_REQUEST, data={"error": "some client error"}
    )
    with pytest.raises(exceptions.BadRequest) as err:
        OneMap("email@example.com", "password").search("307987")
        assert str(err) == "some client error"

    mock_request.return_value = MagicMock(status_code=status.HTTP_400_BAD_REQUEST)
    with pytest.raises(exceptions.BadRequest) as err:
        OneMap("email@example.com", "password").search("307987")
        assert str(err) == "Please ensure request is correct."


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_client_search_server_error(mock_request, mock_connect):
    mock_connect.return_value = None, None
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    with pytest.raises(exceptions.ServerError) as err:
        OneMap("email@example.com", "password").search("307987")
        assert str(err) == "OneMap SG server error. Please try again later."


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_client_search_return_none(mock_request, mock_connect):
    mock_connect.return_value = None, None
    mock_request.return_value = MagicMock(status_code=status.HTTP_301_MOVED_PERMANENTLY)
    onemap = OneMap("email@example.com", "password")
    res = onemap.search("123456")
    assert res is None


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_client_route(mock_request, mock_connect):
    """Should return RouteResult instance."""
    mock_connect.return_value = "some-token", 1234567
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={
            "status_message": "Found route between points",
            "alternative_names": [
                ["COMMONWEALTH AVENUE WEST", "NORTH BUONA VISTA ROAD"]
            ],
            "route_name": ["CLEMENTI AVENUE 2", "ULU PANDAN ROAD"],
            "route_geometry": (
                "yr`oAm`k{dEksAstD~e@iW`e@{UxtAqr@pd@sVrOmItC}GZ}GJwDeSmWkm@gb@qKuEyCw"
                "E}AgHJiH\\kE{BaRoCoEsGcLiE{N{AmQvB{QbFkN|E}FzMcPtQmTh|A_iBfCcDzHcKpJa"
                "Mr\\w_@t\\i`@hb@gg@lAkJRqJg@wJeCoMgQ{f@qHsTuC_FiMsT_S_ViVkPkfAyi@oXiN"
                "q{@q_@qn@cU{SsGgEqAiDeAcTsGcd@eMoF{AoBi@uGkB}d@uMwDoA_EsA{QiG_VyJaSkL"
                "kQuN}CgDqJkKqDsFqE_H}CuE}CyEsBsGcDeKuK}f@}FiJ_FaEkKiEgHcAe~@xMsr@`LqM"
                "rB_En@gAy`@kBkVwE{W_^gbAkHg[aFeQaRe^_Nea@iEwYJkYsAyj@KiRkGglAcDqn@KiU"
                "rDkc@nFkY`Lo]lIeQfJgOfcAyhAzJ}KtPsTjIuQxFaQrBcN|E{u@rDgh@hBuYjDy_@zHo"
                "UbI}O|PwSkDuBiP_K{]cTq_Ack@ixAe|@_L}G{LoHynBujAsh@iZiRqK}|@ig@xg@wo@v"
                "{@_gA~q@g}@fUgZp^{`@gDqLv`@oNfTwH~LcIl@gEy@{PqU_V_`@cuAvHwJt^_MvXgMxC"
                "aD"
            ),
            "route_instructions": [
                ["10", "PANDAN LOOP", 853, 0, 89, "853m", "NE", 65, 1, "SW", 245]
            ],
            "alternative_summaries": [
                {
                    "end_point": "REBECCA ROAD",
                    "start_point": "PANDAN LOOP",
                    "total_time": 761,
                    "total_distance": 8133,
                }
            ],
            "via_points": [[1.311549, 103.749657], [1.32036, 103.800156]],
            "route_summary": {
                "end_point": "REBECCA ROAD",
                "start_point": "PANDAN LOOP",
                "total_time": 740,
                "total_distance": 7957,
            },
            "found_alternative": True,
            "status": 200,
            "via_indices": [0, 140],
            "hint_data": {
                "locations": [
                    "NzgBANtqAQBRBQAAAAAAAAQAAAAAAAAAuQIAAEOcAABoAAAAPQMUABcYLwYAAAEB",
                    "0OUAAF4zAQChAwAABAAAAAwAAABIAAAAdQAAACx9AABoAAAAqCUUAFndLwYCAAEB",
                ],
                "checksum": 585417468,
            },
            "alternative_geometries": [
                (
                    "yr`oAm`k{dEksAstD~e@iW`e@{UxtAqr@pd@sVrOmItC}GZ}GJwDeSmWkm@gb@qKu"
                    "EyCwE}AgHJiH\\kE{BaRoCoEsGcLiE{N{AmQvB{QbFkN|E}FzMcPtQmTh|A_iBfCc"
                    "DzHcKpJaMr\\w_@t\\i`@hb@gg@lAkJRqJg@wJeCoMgQ{f@qHsTuC_FiMsT_S_ViV"
                    "kPkfAyi@oXiNq{@q_@qn@cU{SsGgEqAiDeAcTsGcd@eMoF{AoBi@uGkB}d@uMwDoA"
                    "_EsA{QiG_VyJaSkLkQuN}CgDqJkKqDsFqE_H}CuE}CyEsBsGcDeKuK}f@}FiJ_FaE"
                    "kKiEgHcAe~@xMsr@`LqMrB_En@gAy`@kBkVwE{W_^gbAkHg[aFeQaRe^_Nea@iEwY"
                    "JkYsAyj@KiRkGglAcDqn@KiUrDkc@nFkY`Lo]lIeQfJgOfcAyhAzJ}KtPsTjIuQxF"
                    "aQrBcN|E{u@rDgh@hBuYjDy_@zHoUbI}O|PwSkDuBiP_K{]cTq_Ack@ixAe|@_L}G"
                    "{LoHynBujAsh@iZiRqK}|@ig@xg@wo@v{@_gA~q@g}@fUgZp^{`@gDqLv`@oNfTwH"
                    "~LcIl@gEy@{PqU_V_`@cuAvHwJt^_MvXgMxCaD"
                )
            ],
            "alternative_instructions": [
                [
                    ["10", "PANDAN LOOP", 853, 0, 89, "853m", "NE", 65, 1, "SW", 245],
                    ["8", "JALAN BUROH", 217, 9, 23, "217m", "NE", 50, 1, "SW", 230],
                    ["1", "WEST COAST HIGHWAY", 62, 14, 7, "61m", "E", 92, 1, "W", 272],
                ]
            ],
            "alternative_indices": [0, 159],
        },
    )
    route_result = OneMap("email@example.com", "password").route(
        "1.23,1.01", "1.01,1.23", "drive"
    )
    assert isinstance(route_result, response.RouteResult)


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_client_route_return_none(mock_request, mock_connect):
    mock_connect.return_value = "some-token", 1234567
    mock_request.return_value = MagicMock(status_code=status.HTTP_301_MOVED_PERMANENTLY)
    onemap = OneMap("email@example.com", "password")
    res = onemap.route("1.23,1.01", "1.01,1.23", "drive")
    assert res is None


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_reverse_geocode_svy21(mock_request, mock_connect):
    """Should return GeocodeInfo instance."""
    mock_connect.return_value = "some-token", 1234567
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={
            "GeocodeInfo": [
                {
                    "BUILDINGNAME": "NEW TOWN PRIMARY SCHOOL",
                    "BLOCK": "300",
                    "ROAD": "TANGLIN HALT ROAD",
                    "POSTALCODE": "148812",
                    "XCOORD": "24303.327416",
                    "YCOORD": "31333.331116",
                    "LATITUDE": "1.2996418106402365",
                    "LONGITUDE": "103.80011086725216",
                    "LONGTITUDE": "103.80011086725216",
                }
            ]
        },
    )
    geocode_info = OneMap("email@example.com", "password").reverse_geocode(
        "svy21", (24291.97788882387, 31373.0117224489)
    )
    assert isinstance(geocode_info, response.GeocodeInfo)


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_reverse_geocode_wsg84(mock_request, mock_connect):
    """Should return GeocodeInfo instance."""
    mock_connect.return_value = "some-token", 1234567
    mock_request.return_value = MagicMock(
        status_code=status.HTTP_200_OK,
        data={
            "GeocodeInfo": [
                {
                    "BUILDINGNAME": "NEW TOWN PRIMARY SCHOOL",
                    "BLOCK": "300",
                    "ROAD": "TANGLIN HALT ROAD",
                    "POSTALCODE": "148812",
                    "XCOORD": "24303.327416",
                    "YCOORD": "31333.331116",
                    "LATITUDE": "1.2996418106402365",
                    "LONGITUDE": "103.80011086725216",
                    "LONGTITUDE": "103.80011086725216",
                }
            ]
        },
    )
    geocode_info = OneMap("email@example.com", "password").reverse_geocode(
        "wgs84", (1.3, 103.8)
    )
    assert isinstance(geocode_info, response.GeocodeInfo)


@patch("onemapsg.client.OneMap._connect")
@patch("onemapsg.client.make_request")
def test_reverse_geocode_return_none(mock_request, mock_connect):
    """Should return GeocodeInfo instance."""
    mock_connect.return_value = "some-token", 1234567
    mock_request.return_value = MagicMock(status_code=status.HTTP_301_MOVED_PERMANENTLY)
    geocode_info = OneMap("email@example.com", "password").reverse_geocode(
        "wgs84", (1.3, 103.8)
    )
    assert geocode_info is None
