"""ACT Architects Registration Board checker."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests

from ..constants import ResultKeys, StatusValues
from .base import BaseRegistrationChecker, register_checker


@register_checker
class ACTArchitectsChecker(BaseRegistrationChecker):
    """Checker for ACT Architects Registration Board.

    Unlike the NSW/QLD checkers, this queries an open, ungated Socrata JSON
    endpoint rather than scraping a live site, so it does not need a
    WebDriver. The endpoint has a low query budget before it throttles, so
    the whole register is fetched once and cached on the instance rather
    than queried per person.

    Data is from the ACT Government's open data portal, and is explained here: https://www.data.act.gov.au/Business-and-Industry/Currently-Registered-Architects/5gye-c7hr/about_data
    """

    ACT_ENDPOINT = "https://www.data.act.gov.au/resource/5gye-c7hr.json"
    REQUEST_TIMEOUT_SECONDS = 15

    def __init__(self, driver):
        """Initialize the checker. `driver` is accepted for interface
        compatibility with other checkers but is not used."""
        super().__init__(driver)
        self._records: dict[str, dict[str, Any]] | None = None

    @property
    def registration_body_name(self) -> str:
        """Return the name of the registration body."""
        return "Australian Capital Territory Architects Board"

    def check_registration(self, reg_number: str, **kwargs) -> dict[str, Any]:
        """
        Check registration status with the ACT Architects Registration Board.

        Args:
            reg_number: The registration number to check

        Returns:
            Dictionary with registration status and details
        """
        try:
            if self._records is None:
                self._records = self._fetch_records()

            record = self._records.get(str(reg_number))
            if record is None:
                return {ResultKeys.STATUS: StatusValues.NOT_FOUND}

            return self._build_result(reg_number, record)
        except Exception as e:  # noqa: BLE001 - fail-safe contract shared with nsw/qld checkers
            return self.handle_error(reg_number, e)

    def _fetch_records(self) -> dict[str, dict[str, Any]]:
        """
        Fetch the full ACT architects register once and index it by
        registration number. Retries once on a transient failure.

        Returns:
            Mapping of registration_number -> raw row dict
        """
        params = {"$limit": 5000}
        last_error: Exception | None = None

        for _attempt in range(2):
            try:
                response = requests.get(
                    self.ACT_ENDPOINT,
                    params=params,
                    timeout=self.REQUEST_TIMEOUT_SECONDS,
                )
                response.raise_for_status()
                rows = response.json()
                return {row["registration_number"]: row for row in rows}
            except Exception as e:  # noqa: BLE001 - retried once, then re-raised to the caller
                last_error = e

        assert last_error is not None
        raise last_error

    def _build_result(self, reg_number: str, record: dict[str, Any]) -> dict[str, Any]:
        """
        Build a result dict from a matched register row.

        The dataset has no explicit status field, so status is derived from
        the expiry_date relative to today.

        Args:
            reg_number: The registration number that was searched for
            record: The matched raw row from the register

        Returns:
            Dictionary containing status, name, reg_number, original_status
        """
        expiry_text = record.get("expiry_date", "")
        status = self._status_from_expiry(expiry_text)
        name = f"{record.get('given_names', '')} {record.get('surname', '')}".strip()

        return {
            ResultKeys.STATUS: status,
            ResultKeys.NAME: name,
            ResultKeys.REG_NUMBER: reg_number,
            ResultKeys.ORIGINAL_STATUS: expiry_text,
        }

    @staticmethod
    def _status_from_expiry(expiry_text: str) -> str:
        """Derive a status string from an "expiry_date" like '17 DECEMBER 2026'."""
        try:
            expiry = (
                datetime.strptime(expiry_text.strip().title(), "%d %B %Y")
                .replace(tzinfo=timezone.utc)
                .date()
            )
        except (ValueError, AttributeError):
            return StatusValues.ERROR

        if expiry >= datetime.now(timezone.utc).date():
            return StatusValues.CURRENT_AND_ACTIVE
        return "expired"
