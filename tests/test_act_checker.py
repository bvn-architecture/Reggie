"""Tests for the ACT Architects Registration Board checker."""

from unittest.mock import MagicMock, patch

from reggie.checkers.act import ACTArchitectsChecker
from reggie.constants import (
    KNOWN_UNCHECKED_REGISTRATION_BODIES,
    ResultKeys,
    StatusValues,
)

FAKE_ROWS = [
    {
        "surname": "AIFANTIS",
        "given_names": "NICK",
        "business_location": "BARTON ACT 2600",
        "registration_number": "2227",
        "expiry_date": "17 DECEMBER 2099",
    },
    {
        "surname": "OLDNAME",
        "given_names": "PAST",
        "business_location": "CITY ACT 2601",
        "registration_number": "1000",
        "expiry_date": "1 JANUARY 2000",
    },
]


def _mock_response():
    response = MagicMock()
    response.json.return_value = FAKE_ROWS
    response.raise_for_status.return_value = None
    return response


def test_act_checker_registration_body_name():
    checker = ACTArchitectsChecker(driver=None)
    assert (
        checker.registration_body_name
        == "Australian Capital Territory Architects Board"
    )


def test_act_checker_not_in_known_unchecked_bodies():
    assert (
        "Australian Capital Territory Architects Board"
        not in KNOWN_UNCHECKED_REGISTRATION_BODIES
    )


@patch("reggie.checkers.act.requests.get")
def test_act_checker_finds_current_registration(mock_get):
    mock_get.return_value = _mock_response()
    checker = ACTArchitectsChecker(driver=None)

    result = checker.check_registration("2227")

    assert result[ResultKeys.STATUS] == StatusValues.CURRENT_AND_ACTIVE
    assert result[ResultKeys.NAME] == "NICK AIFANTIS"
    assert result[ResultKeys.REG_NUMBER] == "2227"


@patch("reggie.checkers.act.requests.get")
def test_act_checker_finds_expired_registration(mock_get):
    mock_get.return_value = _mock_response()
    checker = ACTArchitectsChecker(driver=None)

    result = checker.check_registration("1000")

    assert result[ResultKeys.STATUS] == "expired"


@patch("reggie.checkers.act.requests.get")
def test_act_checker_not_found(mock_get):
    mock_get.return_value = _mock_response()
    checker = ACTArchitectsChecker(driver=None)

    result = checker.check_registration("99999")

    assert result[ResultKeys.STATUS] == StatusValues.NOT_FOUND


@patch("reggie.checkers.act.requests.get")
def test_act_checker_caches_fetch_across_calls(mock_get):
    mock_get.return_value = _mock_response()
    checker = ACTArchitectsChecker(driver=None)

    checker.check_registration("2227")
    checker.check_registration("1000")

    assert mock_get.call_count == 1


@patch("reggie.checkers.act.requests.get")
def test_act_checker_handles_network_error(mock_get):
    mock_get.side_effect = ConnectionError("boom")
    checker = ACTArchitectsChecker(driver=None)

    result = checker.check_registration("2227")

    assert result[ResultKeys.STATUS] == StatusValues.ERROR
    assert result[ResultKeys.REG_NUMBER] == "2227"
